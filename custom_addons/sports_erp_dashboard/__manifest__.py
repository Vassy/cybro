{
    'name': 'Sports ERP Dashbaord',
    'version': '15.0.1.0.0',
    'author': 'Ljutzkanov Limited',
    'website': 'www.ljutzkanov.ltd',
    'description': """

    """,
    'depends': ['website', 'portal', 'organisation'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'views/survey.xml',
        # 'views/template.xml',
        # 'views/survey_templates.xml',
        # 'views/calculated_metric_operator.xml',
        # 'views/calculated_metric_operator.xml',
        'data/data.xml',
        # 'data/website_menus.xml',
        'views/res_partner.xml',
        'views/portal_template.xml',
        'views/header.xml',
        'views/coach.xml',
        'views/athletes.xml',
        'views/venues.xml',
        'views/parents.xml',
        'views/groups.xml',
        'views/discipline.xml',
        'views/fan.xml',
        'views/home_edits.xml',
        'views/home_template.xml',
        'views/subscription_template.xml',
        'views/chat_hub.xml',
        'views/dashboard.xml',
        'views/subscription_plan.xml',
        'views/subscription_contract.xml',
        'views/subscription_product.xml',
        'views/subscription_customer.xml',
        'views/settings_dashboard.xml',
        'views/subscription_details.xml',
        'views/profile_template.xml',
        'views/subscription_organisation.xml',
        'views/events_template.xml',
        'views/event_template_page.xml',
        'views/event_stage.xml',
        'views/event_tag_category.xml',
        'views/documents.xml',
        'views/subscription_home.xml',
        'views/booking_home.xml',
        'views/footer.xml',
        'views/login.xml',
        'views/home_edit_web.xml'

    ],
    'assets': {
        'web.assets_backend': [
            # 'survey_extension/static/src/js/body_map_widget.js',
            # 'survey_extension/static/src/js/survey_report.js'
        ],
        'web.assets_frontend': [
            # 'sports_erp_dashboard/static/src/xml/assets.xml',
            'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
            # 'https://cdn.jsdelivr.net/jquery/latest/jquery.min.js',
            # 'https://cdn.jsdelivr.net/momentjs/latest/moment.min.js',
            'https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.min.js',
            'https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.css',
            'sports_erp_dashboard/static/src/js/coach.js',
            'sports_erp_dashboard/static/src/js/event.js',
            'sports_erp_dashboard/static/src/js/loader.js',
            'sports_erp_dashboard/static/src/js/image_edit.js',
            # 'sports_erp_dashboard/static/src/css/style_new.css',
            'sports_erp_dashboard/static/src/css/style.min.css',
            'https://cdn.jsdelivr.net/npm/html-duration-picker@latest/dist/html-duration-picker.min.js',
            # # 'https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css',
            # # 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.css',
            # 'https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js',
            # # 'sports_erp_dashboard/static/src/scss/**/*',
        ],
        'web.assets_qweb': [
            # 'survey_extension/static/src/xml/body_map_view.xml',
            # 'survey_extension/static/src/xml/survey_report.xml',
        ],
    },
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}