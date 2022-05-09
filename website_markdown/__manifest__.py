# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Website Markdown",
    # any module necessary for this one to work correctly
    'depends': ['base',],
        'external_dependencies': {
        'python': ['bs4','markdown', ],
    },
}
