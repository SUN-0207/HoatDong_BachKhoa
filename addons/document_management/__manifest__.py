{
    "name": "Document Management",
    "description": """Manage and Generate Document Into Word""",
    "summnary": "Document Management",
    "category": "Hcmut",
    "version": "16.0.2",
    'author': 'TST',
    'website': "https://www.odoo.com",
    "depends": ['base','base_setup','manage_user_info','web'],
    "data": [
        'security/ir.model.access.csv',
        'data/document_data.xml',
        'views/temporary_document_views.xml',
        'views/document_views.xml',
        'views/document_type_views.xml',
        'views/document_number_book_views.xml',
        'wizard/document_reset_number_book_wizard_views.xml',
        'views/document_management_menuitem.xml'
    ],
    'assets': {
       'web.assets_backend': [
            'document_management/static/src/js/reset_modal.js',
            'document_management/static/src/xml/reset_button.xml',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}