# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2022- Vertel AB (<https://vertel.se>).
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
    'name': 'Workplace: Communication Center Jitsi',
    'version': '16.0.0.0.1',
    # Version ledger: 14.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'summary': 'Setup communication with Jitsi.',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity',
    'description': """
    Setup communication with Jitsi.
    """,
    #'sequence': '1',
    'sequence': '280',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-digitalworkplace/communication_center_jitsi',
    'images': ['static/description/banner.png'], # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-digitalworkplace',
    # Any module necessary for this one to work correctly
    'depends': ['base', 'communication_center_calendar_online_meeting', 'website', 'communication_center_website_event_online_meeting'],
    # always loaded
    'data': [
        'views/res_config_settings_view.xml',
        # 'views/assets.xml',
        'views/jitsi_controller.xml',
        'views/calendar_view.xml',
        'views/event_view.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'communication_center_jitsi/static/src/js/meeting_settings.js',
            'communication_center_jitsi/static/src/js/external_api.js',
            'communication_center_jitsi/static/src/css/controller_style.css',
        ]
    },
    'qweb': [
        'static/src/xml/calendar_view_templet.xml',
    ],
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
