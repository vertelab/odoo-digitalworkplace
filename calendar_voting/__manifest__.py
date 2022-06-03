
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Calendar Voting",
    # any module necessary for this one to work correctly
    'depends': ['base', 'calendar', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/calendar_voting_view.xml',
        'data/mail_data.xml',
        'views/controller_voting_view.xml',
        'views/assets.xml',
    ]
}