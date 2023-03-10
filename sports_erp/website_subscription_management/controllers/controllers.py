# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import fields
from odoo.http import request
import logging
from odoo.exceptions import ValidationError

_logger=logging.getLogger(__name__)
from odoo import http
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_sale.controllers.main import WebsiteSale
from datetime import datetime, timedelta


class Website(WebsiteSale):

    record_id=None

    @http.route('/my/subscriptions', auth='user',website=True,type='http')
    def subscr_table(self, **kw):

        user_id = request.env['res.users'].sudo().browse(request._uid)
        subscriptions=request.env['subscription.subscription'].sudo().search([('customer_name','=',user_id.partner_id.id)])
        return request.render('website_subscription_management.portal_my_subscription',{'subscriptions':subscriptions})


    @http.route('/my/subscriptions/<model("subscription.subscription"):myid>/', auth='user',website=True,type='http')
    def subscr_detail_refresh(self, myid,**kw):
        if myid:
            done=myid.renewe_subscription()
            return request.redirect('/my/subscriptions')

    @http.route('/my/subscriptions/<model("subscription.subscription"):myid>/', auth='user',website=True,type='http')
    def subscr_detail(self,myid,**kw):
        allow_cancel = request.env["ir.default"].get('res.config.settings',
                                                  'allow_cancel')
        allow_freeze = request.env["ir.default"].get('res.config.settings',
                                                  'allow_freeze')
        if myid:
           date=None
           select=dict(myid._fields['source'].selection).get(myid.source)
           N = myid.sub_plan_id.notification_days #No. of days before you get notification
           if myid.end_date:
            date_list=list(map(int,myid.end_date.strftime("%Y-%m-%d").split("-")))
            date_N_days_ago = datetime(date_list[0],date_list[1],date_list[2]) - timedelta(days=N)
            date=date_N_days_ago.strftime('%Y-%m-%d')
            condition=date==datetime.now().strftime('%Y-%m-%d')

            if date==datetime.now().strftime('%Y-%m-%d'):
                request.env['website'].sudo().notification_mail_send()
           else:
             condition=False
           reason_record=request.env['subscription.reasons'].sudo().search([])
           subscription_message=request.env['subscription.configuration'].sudo().search([])
        return request.render(
            'website_subscription_management.my_subscription_detail', {
                'detail':myid, 'select':select, 'condition':condition,
                'reasons':reason_record, 'message':subscription_message,
                'allow_cancel': allow_cancel, 'allow_freeze': allow_freeze})


    @http.route('/website/json/controller',type='json',website=True,auth='user')
    def json_controller(self,renew,**kw):
        if renew:
            done=request.env['subscription.subscription'].sudo().browse([int(renew)]).renewe_subscription()
            return True
        else:
            return False

   


    @http.route('/example/reason',methods=['POST'],type='http',auth='user',website=True,csrf=False)
    def render_detail(self,**kw):
        subscription_obj=request.env['subscription.subscription'].sudo().browse(int(kw['sub_plan_record_id']))

        subscription_obj.reason = kw['reason_id'] + kw['message'] if kw['message'] else ""
        if subscription_obj.state in ['in_progress']:
            subscription_obj.state='close'
            return request.redirect('/my/subscriptions')

        elif subscription_obj.state in ['draft']:
            if subscription_obj.get_cancel_sub():
                return request.redirect('/my/subscriptions')

    @http.route('/subscription/freeze', methods=['POST'], type='http',
                auth='user', website=True, csrf=False)
    def freeze_subscription(self, **kw):
        subscription_obj = request.env[
            'subscription.subscription'].sudo().browse(
            int(kw['sub_plan_record_id']))
        contract = subscription_obj.contract_id
        if subscription_obj.freeze_count >= contract.allowed_freeze_count:
            raise ValidationError('Reached Allowed Freeze Limit')
        frozen_stage = request.env['subscription.stage'].sudo().search(
            [('name', 'ilike', 'Frozen')])
        obj_freeze = request.env['subscription.freeze'].sudo().create({
            'subscription_id': subscription_obj.id,
            'start_date': fields.Date.today(),
            'end_date': fields.Date.add(fields.Date.today(),
                                        days=contract.freeze_period)
        })
        subscription_obj.sudo().write({
            'state': 'frozen',
            'stage_id': frozen_stage.id,
            'in_frozen_stage': True,
            'freeze_id': obj_freeze.id,
            'freeze_count': subscription_obj.freeze_count + 1,
        })
        if subscription_obj.end_date:
            subscription_obj.write({
                'end_date': fields.Date.add(subscription_obj.end_date,
                                            days=contract.freeze_period),
            })
        if subscription_obj.next_payment_date:
            subscription_obj.write({
                'next_payment_date': fields.Date.add(
                    subscription_obj.next_payment_date,
                    days=contract.freeze_period),
            })
        return request.redirect('/my/subscriptions')

    @http.route()
    def address(self, **kw):
        order = request.website.sale_get_order()
        if bool(order.order_line.mapped('product_id').filtered(
                lambda p: p.activate_subscription==True)) and \
                request.env.user.id == request.website.user_id.id:
            return request.redirect('/web/login?redirect=/shop/cart')

        values = super(Website, self).address(**kw)
        return values

    @http.route('/check/product_variant/subscription',
                type='json', website=True, auth='public')
    def json_count_div(self, product_id, **kw):
        if request.env['product.product'].sudo().browse(
                [int(product_id)]).activate_subscription:
            return True
        else:
            return False
