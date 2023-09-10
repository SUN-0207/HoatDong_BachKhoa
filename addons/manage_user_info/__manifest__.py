{
    "name": "Manage User Informantion",
    "description": """Manage User Informantion""",
    "summary": "Manage User Informantion",
    "category": "Manage Info",
    "version": "16.0.2",
    'author': 'TST',
    'website': "https://www.odoo.com",
    "depends": ['base_setup'],
    "data": [
        'views/user_info_views.xml',
        'views/user_account_info_views.xml',
        'views/user_info_department_views.xml',
        'views/user_info_class_views.xml',
        'views/user_info_major_views.xml',
        'views/user_info_menuitem.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/manage_user_info/static/src/css/invalid.css',
            '/manage_user_info/static/src/js/invalid_field.js',
        ],
    },
   
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
