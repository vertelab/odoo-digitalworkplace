# -*- coding: utf-8 -*-
#################################################################################
{
    "name": "Odoo Chatter Message Edit And Delete",
    "summary": "Edit and Delete option for chatter's Message & Log Note",
    "category": "Discuss",
    "version": "14.0.1.0.0",
    "sequence": 1,
    "author": "Vertel AB Ltd.",
    "website": "https://vertel.se",
    "description": """
Log Note
====================
This module will add edit/delete option in chatter's message & log note .
    """,
    "depends": ['mail'],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/assets.xml',
        'views/mail_message_views.xml',
        'wizard/edit_message_log_note_views.xml',
        'views/res_config_settings_views.xml',
    ],
    "qweb": [
        'static/src/components/message/message.xml'
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
    "pre_init_hook": "pre_init_check",
}
