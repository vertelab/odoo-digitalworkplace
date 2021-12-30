# -*- coding: utf-8 -*-
{
    'name': "Readit",
    'summary': "A company forum where any topic can be discussed.",
    'description': """
    Readit
    A company forum where any topic can be discussed.
    Each post's content is render within the Kanban view grouped by Forum subject.
    
    Only Settings Administrators can edit or delete content.
    
    Users may edit the information regarding their post:
    - Post Title
    - Post's Forum
    Users may add content to their posts, but not remove anything.
    Comments last forever, so use your best judgement.

    URLs render as:
    1. Title (hyperlink to the original URL)
    2. Description
    3. Image or Favicon
    """,

    'author': "Odoo",
    'website': "http://www.odoo.com",

    'application': True,
    'installable': True,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'license': 'AGPL-3',
    'category': 'Discuss',
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['contacts', 'renderlistcontent'],
    'images': ['static/description/banner.png'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
