{
    "name": "Document Management",
    "description": """Manage and Generate Document Into Word""",
    "summnary": "Document Management",
    "category": "Hcmut",
    "version": "16.0.2",
    'author': 'TST',
    'website': "https://www.odoo.com",
    "depends": ['base','base_setup'],
    "data": [
        'security/ir.model.access.csv',
        'views/temporary_document_views.xml',
        'views/document_management_menuitem.xml'
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}