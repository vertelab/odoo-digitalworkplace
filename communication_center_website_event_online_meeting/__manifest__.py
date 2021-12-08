# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Event Online Meeting",
    'summary': """Setup a link for your online event""",
    'description': """
        Setup a link for your online link for events
    """,
    'category': 'Productivity/Calendar',
    'sequence': 280,
    'version': '14.0.0.0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'communication_center_jitsi', 'event', 'website_event'],

    # always loaded
    'data': [
        'views/event_view.xml',
        'data/email_template_data.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}
