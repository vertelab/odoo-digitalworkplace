# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Calendar Online Meeting",
    'summary': """Setup a link for your online meeting""",
    'description': """
        Setup a link for your online meeting
    """,
    'category': 'Productivity/Calendar',
    'sequence': 280,
    'version': '14.0.0.0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'calendar'],

    # always loaded
    'data': [
        'views/res_config_settings_view.xml',
        'views/calendar_view.xml',
        'data/mail_data.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}
