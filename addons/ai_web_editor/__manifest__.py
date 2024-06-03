# -*coding: utf-8 -*-
#################################################################################
# Author      : CFIS (<https://www.cfis.store/>)
# Copyright(c): 2017-Present CFIS.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://www.cfis.store/>
#################################################################################

{
    "name": "Odoo Editor AI | Editor AI Autocompleter | Open AI Editor | AI Autocompleter | Editor AI | Content Generator AI",
    "summary": """
        This module enables users to quickly create content, correct grammar errors, translate text to english,
        or ask AI any question they can think of from within the Powerbox commands of the Odoo Editor.
    """,
    "version": "16.0.1",
    "description": """
        This module enables users to quickly create content, correct grammar errors, translate text to english,
        or ask AI any question they can think of from within the Powerbox commands of the Odoo Editor.
        Odoo Editor AI
        Editor AI Autocompleter
        Open AI Editor
        AI Autocompleter
        Editor AI 
        Content Generator AI
    """,    
    "author": "CFIS",
    "maintainer": "CFIS",
    "license" :  "Other proprietary",
    "website": "https://www.cfis.store",
    "images": ["images/ai_web_editor.png"],
    "category": "Extra Tools",
    "depends": [
        "base",
        "web_editor",
    ],
    "data": [
        "views/assets.xml",             
        "views/res_config_settings.xml",             
    ],
    "assets": {
        "web.assets_backend": [
            "ai_web_editor/static/src/lib/*.js",
        ],
        'web_editor.assets_wysiwyg': [
            "ai_web_editor/static/src/js/*.js",
            "ai_web_editor/static/src/xml/*.xml",
        ]
    },    
    "installable": True,
    "application": True,
    "price"                 :  29,
    "currency"              :  "EUR",
    "pre_init_hook"         :  "pre_init_check",
}