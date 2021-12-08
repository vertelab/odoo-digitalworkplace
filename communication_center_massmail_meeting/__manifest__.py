# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Mass Mailing Meeting Link",
    'summary': """Setup Jitsi for Mass Mailing""",
    'description': """
        Setup Jitsi for Mass Mailing
    """,
    'category': 'Productivity/VOIP',
    'sequence': 280,
    'version': '14.0.0.0.1',
    'depends': ['base', 'communication_center_jitsi', 'mass_mailing'],
    'data': [
        'views/mailing_view.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}
