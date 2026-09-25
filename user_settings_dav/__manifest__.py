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
    'name': 'Workplace: User Settings Dav',
    'version': '0.1',
    # Version ledger: 14.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'summary': '',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity',
    'description': """
    
    """,
    #'sequence': '1',
    'author': 'Vertel Sverige AB',
    'website': 'https://vertel.se/apps/odoo-digitalworkplace/user_settings_dav',
    'images': ['static/description/banner.png'],  # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-digitalworkplace',
    # Any module necessary for this one to work correctly
    #
    # 'calendar' is REQUIRED: data/collection.xml seeds a dav.collection for
    # calendar events and references calendar.model_calendar_event,
    # calendar.field_calendar_event__name/__start/__stop/__users. Odoo loads
    # data files before the dependency graph is fully resolved, so without
    # 'calendar' in depends the xmlids are not yet in ir.model.data and the
    # install aborts with:
    #   ValueError: External ID not found in the system:
    #               calendar.model_calendar_event
    #   ParseError: while parsing .../user_settings_dav/data/collection.xml:4
    # (verified on vixner 2026-09-24).
    'depends': ['base_dav', 'calendar'],
    'data': [
        'views/user_collection_views.xml',
        'views/assets.xml',
        'data/collection.xml',
    ],
    # ------------------------------------------------------------------
    # CalDAV-spår (uppdaterad 2026-09-24)
    #
    # Den tidigare kommentaren här påstod "INSTALLABLE: False" med hänvisning
    # till att modulen skulle registrera /.well-known/caldav och kollidera med
    # calendar_caldav. Det stämmer INTE för denna modul:
    #   - user_settings_dav har ingen controllers/-katalog och registrerar
    #     ingen route alls.
    #   - Den lägger bara till dav_collection_ids på res.users och en flik i
    #     användarformuläret, plus ett dav.collection för kalenderhändelser.
    # Kollisionen mellan /.well-known/caldav gäller base_dav vs
    # calendar_caldav — inte denna modul. Kommentaren och koden sade emot
    # varandra (False vs True); koden har varit True hela tiden.
    #
    'installable': True,
    'auto_install': False,
}
