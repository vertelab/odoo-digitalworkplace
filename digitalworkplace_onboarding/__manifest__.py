# -*- coding: utf-8 -*-
{
    'name': 'Chatt & web-möte i Vertel',
    'version': '18.0.1.0.0',
    'summary': 'Onboardingskurs: chatt (Matrix) och web-möte (Jitsi)',
    'description': """
Lär dig chatta i kanaler, starta videomöten och bjuda in externa deltagare.
""",
    'author': 'Vertel AB',
    'website': 'https://vertel.se',
    'license': 'LGPL-3',
    'category': 'Website/eLearning',
    'depends': ['website_slides'],
    'data': [
        'views/slide_channel_data.xml',
    ],
    'demo': [
        'demo/slide_slide_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
