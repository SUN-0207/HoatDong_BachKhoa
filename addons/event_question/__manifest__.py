{
    "name": "Event Questions",
    "description": """Event custom questions""",
    "summary": "Event custom question addon module",
    "version": "16.0.2",
    'author': 'TST',
    'website': "https://www.odoo.com",
    "depends": [
        'base',
        'base_setup',
        'web', 
        'event',
        'manage_activity',
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/event_views.xml',
        'views/event_question_views.xml',
        'views/event_registration_views.xml',
        'wizard/event_registration_wizard_views.xml',
        'wizard/event_registration_wizard_answers.xml'
    ],
    'assets': {
       'web.assets_backend': [
            'event_question/static/src/scss/styles.scss'
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}