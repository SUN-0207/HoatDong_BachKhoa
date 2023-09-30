{
    "name": "Manage User Informantion",
    "description": """Manage User Informantion""",
    "summary": "Manage User Informantion",
    "category": "Hcmut",
    "version": "16.0.2",
    'author': 'TST',
    'website': "https://www.odoo.com",
    "depends": ['base','base_setup', 'web','auth_oauth' ],
    "data": [
        'security/user_security.xml',
        'security/ir.model.access.csv',
        'data/user_info_address_data.xml',
        'data/department.xml',
        'data/major.xml',
        'data/class.xml',
        'data/user_admin_account.xml',
        'views/res_users.xml',
        'views/user_info_department_views.xml',
        'views/user_info_major_views.xml',
        'views/user_info_class_views.xml',
        'views/user_info_views.xml',
        'views/user_info_menuitem.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'manage_user_info/static/src/js/*',
            'manage_user_info/static/src/scss/*'
        ],
        'qweb': [
            'manage_user_info/static/src/xml/*',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
