# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2022- Vertel Sverige AB (<https://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Workplace: Communication Center SIP',
    'version': '18.0.1.0.1',
    # Version ledger: 14.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'summary': 'Make calls using a VOIP system.',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity',
    'description': '''
Communication Center SIP
========================

    Allows to make call from next activities or with click-to-dial.

    Features:

        - Guided Wizards: Step-by-step dialogs for data entry.
        - UI Integration: Extends 5 view(s) in the Odoo interface.
        - Extends Odoo: Builds on mail.activity, mail.activity.type, voip.configurator, voip.phonecall.
    ''',
    #'sequence': '1',
    'sequence': '280',
    'author': 'Vertel Sverige AB',
    'website': 'https://vertel.se/apps/odoo-digitalworkplace/communication_center_sip',
    'images': ['static/description/banner.png'], # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel Sverige AB',
    'repository': 'https://github.com/vertelab/odoo-digitalworkplace',
    # Any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'web', 'phone_validation'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
        'views/res_users_views.xml',
        'views/voip_phonecall_views.xml',
        'data/mail_activity_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'communication_center_sip/static/lib/sip.js',
            'communication_center_sip/static/src/js/*.js',
            'communication_center_sip/static/src/models/activity/activity.js',
            'communication_center_sip/static/src/scss/call_center_field.scss',
            'communication_center_sip/static/src/scss/voip.scss',
            'communication_center_sip/static/src/xml/*.xml',
        ],
    },
    'application': True,
}
