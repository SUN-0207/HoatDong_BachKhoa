{
    "name": "Manage User Informantion",
    "description": """Manage User Informantion""",
    "summary": "Manage User Informantion",
    "version": "16.0.1",
    'author': 'TST',
    'website': "https://www.odoo.com",
    "depends": ['base_setup'],
    "data": [
        'views/user_info_class_views.xml',
        'views/user_info_department_views.xml',
        'views/user_info_major_views.xml',
        'views/user_info_menuitem.xml',
        'views/user_info_views.xml'
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
