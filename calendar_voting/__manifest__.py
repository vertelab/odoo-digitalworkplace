
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Calendar Voting",
    # any module necessary for this one to work correctly
    'depends': ['base', 'calendar'],
    'data': [
        'security/ir.model.access.csv',
        'views/calendar_voting_view.xml',
    ]
}