{
    "name": "Manage Activity",
    "description": """Manage Activity""",
    "summary": "Manage Activity",
    "version": "16.0.2",
    'author': 'TST',
    'website': "https://www.odoo.com",
    "depends": [
        'base',
        'base_setup',
        'manage_user_info', 
        'event', 
        'website',
        'website_partner',
        'website_mail',],
    "data": [
        'security/ir.model.access.csv',
        'data/event_data.xml',
        'views/event_type_views.xml',
        'views/event_ticket_views.xml',
        'views/event_event_kanban_custom.xml',
        'views/event_event_views.xml',
        'views/event_registration_page_views.xml',
        'views/event_registration_views.xml',
        'wizard/event_registration_wizard_views.xml',
        'views/event_menuitem.xml'
    ],
    'assets': {
       'web.assets_backend': [
            'manage_activity/static/src/scss/kanban.scss',
            'manage_activity/static/src/scss/website_kanban.scss',
        ],
        'web.assets_frontend': [
            'manage_activity/static/src/js/custom_website_event.js',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}