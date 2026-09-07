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
    'name': 'Workplace: Website Immich',
    'version': '0.1',
    'summary': 'Find images from your Immich server',
    'category': 'Productivity',
    'description': """
Explore the photo library of your self-hosted Immich server and find
images to use in Odoo. An Immich search bar is added to the image
library modal, just like Unsplash integration.
    """,
    'author': 'Vertel Sverige AB',
    'website': 'https://vertel.se/apps/odoo-digitalworkplace/website_immich',
    'license': 'AGPL-3',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-digitalworkplace',
    'depends': ['base_setup', 'web_editor', 'html_editor', 'website'],
    'data': [
        'views/res_config_settings_view.xml',
    ],
    'demo': [
        'demo/immich_demo.xml',
    ],
    'assets': {
        'html_editor.assets_media_dialog': [
            'website_immich/static/src/media_dialog/**/*',
            'website_immich/static/src/immich_credentials/**/*',
            'website_immich/static/src/immich_error/**/*',
            'website_immich/static/src/immich_service.js',
        ],
        'web_editor.assets_media_dialog': [
            'website_immich/static/src/media_dialog_legacy/**/*',
            'website_immich/static/src/immich_credentials/**/*',
            'website_immich/static/src/immich_error/**/*',
            'website_immich/static/src/immich_service.js',
        ],
        'web.qunit_suite_tests': [
            'website_immich/static/tests/legacy/**/*',
        ],
        'web.assets_unit_tests': [
            'website_immich/static/tests/**/*',
            ('remove', 'website_immich/static/tests/legacy/**/*'),
        ],
    },
    'images': ['static/description/banner.png'],
    'auto_install': False,
}
