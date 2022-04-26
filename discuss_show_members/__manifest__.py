# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "Show Discuss Members",
    "summary": "Show Discuss Memebers",
    "version": "14.0.0.1",
    'category': 'Dicuss',
    "website": "https://vetelab.com",
    'author': 'Vertel AB',
    "license": "AGPL-3",
    "description": """
        Show Discuss Members in Channels
    """,
    "depends": [
        "mail",
    ],
    "data": [
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/components/discuss/discuss.xml',
        'static/src/components/thread_view/thread_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'LGPL-3',
}