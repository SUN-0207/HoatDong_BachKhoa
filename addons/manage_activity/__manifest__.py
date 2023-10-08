{
    "name": "Manage Activity",
    "description": """Manage Activity""",
    "summary": "Manage Activity",
    "version": "16.0.2",
    'author': 'TST',
    'website': "https://www.odoo.com",
    "depends": ['base','base_setup'],
    "data": [
        'security/ir.model.access.csv',
        'views/activity_activity_views.xml',
        'views/activity_menuitem.xml'
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
