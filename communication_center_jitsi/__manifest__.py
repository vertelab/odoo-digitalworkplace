# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Communication Center Jitsi",
    'summary': """Setup communication with Jitsi""",
    'description': """
        Setup communication with Jitsi
    """,
    'category': 'Productivity/VOIP',
    'sequence': 280,
    'version': '14.0.0.0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'communication_center_calendar_online_meeting'],

    # always loaded
    'data': [
        'views/res_config_settings_view.xml',
        'views/assets.xml',
        'views/testing_controller.xml',
    ],
    'qweb': [
        'static/src/xml/calendar_view_templet.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}
