
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Calendar Voting",
    'summary': """Ability to vote for which day a meeting in Odoo should be hold""",
    'description':"""
        Ability to vote for which day a meeting in Odoo should be hold
    """,
    'category': 'Productivity/VOIP',
    'sequence': 280,
    'version': '14.0.0.0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'calendar', 'website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/calendar_voting_view.xml',
        'data/mail_data.xml',
        'views/controller_voting_view.xml',
        'views/assets.xml',
    ]
}
