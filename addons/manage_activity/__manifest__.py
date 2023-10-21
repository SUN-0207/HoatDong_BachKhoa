{
    "name": "Manage Activity",
    "description": """Manage Activity""",
    "summary": "Manage Activity",
    "version": "16.0.2",
    'author': 'TST',
    'website': "https://www.odoo.com",
    "depends": ['base','base_setup','event', 'manage_user_info'],
    "data": [
        'security/ir.model.access.csv',
        'views/event_event_views.xml',
        'views/event_menuitem.xml',
        'data/event_data.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
