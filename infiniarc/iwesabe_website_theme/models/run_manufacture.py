from collections import defaultdict
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.osv import expression
from odoo.addons.stock.models.stock_rule import ProcurementException
from odoo.tools import float_compare, OrderedSet


class StockRuleOrderId(models.Model):
    _inherit = 'stock.rule'


    @api.model
    def _run_manufacture(self, procurements):
        productions_values_by_company = defaultdict(list)
        errors = []
        i = 0
        for procurement, rule in procurements:
            if float_compare(procurement.product_qty, 0, precision_rounding=procurement.product_uom.rounding) <= 0:
                # If procurement contains negative quantity, don't create a MO that would be for a negative value.
                continue
            # update the current bom if the mo is from customiztion page
            if (procurement.values.get('cust_bom_ids',False)):
                bom = procurement.values.get('cust_bom_ids')[i]
                i += 1
            else:
                bom = rule._get_matching_bom(procurement.product_id, procurement.company_id, procurement.values)

            productions_values_by_company[procurement.company_id.id].append(rule._prepare_mo_vals(*procurement, bom))
        if errors:
            raise ProcurementException(errors)
        if (procurement.values.get('cust_bom_ids'),False):
            if productions_values_by_company:
                for rec in list(productions_values_by_company.values())[0]:
                    rec['is_customize'] = True
        for company_id, productions_values in productions_values_by_company.items():
            # create the MO as SUPERUSER because the current user may not have the rights to do it (mto product launched by a sale for example)
            productions = self.env['mrp.production'].with_user(SUPERUSER_ID).sudo().with_company(company_id).create(productions_values)
            self.env['stock.move'].sudo().create(productions._get_moves_raw_values())
            self.env['stock.move'].sudo().create(productions._get_moves_finished_values())
            productions._create_workorder()
            productions.filtered(lambda p: (not p.orderpoint_id and p.move_raw_ids) or\
                (p.move_dest_ids.procure_method != 'make_to_order' and not p.move_raw_ids and not p.workorder_ids)).action_confirm()

            for production in productions:
                origin_production = production.move_dest_ids and production.move_dest_ids[0].raw_material_production_id or False
                orderpoint = production.orderpoint_id
                if orderpoint and orderpoint.create_uid.id == SUPERUSER_ID and orderpoint.trigger == 'manual':
                    production.message_post(
                        body=_('This production order has been created from Replenishment Report.'),
                        message_type='comment',
                        subtype_xmlid='mail.mt_note')
                elif orderpoint:
                    production.message_post_with_view(
                        'mail.message_origin_link',
                        values={'self': production, 'origin': orderpoint},
                        subtype_id=self.env.ref('mail.mt_note').id)
                elif origin_production:
                    production.message_post_with_view(
                        'mail.message_origin_link',
                        values={'self': production, 'origin': origin_production},
                        subtype_id=self.env.ref('mail.mt_note').id)
        return True


