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
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'Workspace: Discuss Show Members',
    'version': '1.0.0',
    # Version ledger: 14.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'summary': 'Show Discuss Members.',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity',
    'description': '''
Discuss Show Members
====================

    Show Discuss Members.

    Features:

        - UI Integration: Extends 1 view(s) in the Odoo interface.
        - Extends Odoo: Builds on mail.channel.
    ''',
    #'sequence': '1',
    'author': 'Vertel Sverige AB',
    'website': 'https://vertel.se/apps/odoo-digitalworkplace/discuss_show_members',
    'images': ['static/description/banner.png'], # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel Sverige AB',
    'repository': 'https://github.com/vertelab/odoo-digitalworkplace',
    # Any module necessary for this one to work correctly
    'depends': ['mail',],
    'assets': {
        'web.assets_backend': [
            'discuss_show_members/static/src/components/**/*',
            'discuss_show_members/static/src/scss/style.scss',
        ],
    },
    # UNPORTED: mail.channel was renamed discuss.channel in 18.0 and the
    # legacy OWL client (odoo.define components, owl="1" templates) was
    # replaced. The module is Odoo-17 code — it crashes on a fresh 18.0
    # install with "Model 'mail.channel' does not exist" — and there is
    # nothing to inherit from in 19.0/20.0. Porting it means rewriting the
    # client patch against the new Discuss, which is a feature, not a port.
    'installable': False,
    'application': False,
    # Disable auto_install so it is only installed explicitly.
    'auto_install': False,
    'license': 'LGPL-3',
}
