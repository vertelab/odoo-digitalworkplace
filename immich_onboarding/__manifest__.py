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
    'name': 'Workplace: Immich Onboarding',
    'version': '18.0.1.0.0',
    'summary': 'Onboarding course: use your Immich photo library from Odoo',
    'category': 'Productivity',
    'description': """
An onboarding course for the Workplace Immich integration.

The course walks a user through connecting their Immich server, finding
photos by content or person, and inserting them into Odoo content — the
image library modal, website pages, knowledge articles and documents.

It is a course only: installing it does not enable any Immich feature.
The features live in ``website_immich``; this module merely teaches them,
following the same convention as ``digitalworkplace_onboarding`` and
``user_mail_onboarding``.
    """,
    'author': 'Vertel Sverige AB',
    'website': 'https://vertel.se/apps/odoo-digitalworkplace/immich_onboarding',
    'license': 'AGPL-3',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-digitalworkplace',
    'depends': [
        'website_slides',
        'website_immich',
    ],
    'data': [
        'data/slide_channel_data.xml',
        'views/slide_channel_views.xml',
    ],
    'demo': [
        'demo/immich_onboarding_demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
