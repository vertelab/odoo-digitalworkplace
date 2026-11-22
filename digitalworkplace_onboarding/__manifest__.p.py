# -*- coding: utf-8 -*-
{
    'name': 'Chatt & web-möte i Vertel',
    'version': '18.0.2.0.0',
    'summary': 'Onboardingskurs: chatt (Matrix) och web-möte (Jitsi)',
    'description': """
Lär dig chatta i kanaler, starta videomöten och bjuda in externa deltagare.

Kursen har fem sektioner:
  1. Vad det är och varför
  2. Så kopplar du upp dig
  3. Chatt i vardagen
  4. Web-möte i vardagen
  5. Manuellt test — verifiera att det fungerar

Allt innehåll ligger i data/ (inte demo/) och skapas därmed även i
produktionsdatabaser som körs med --without-demo=all.
""",
    'author': 'Vertel Sverige AB',
    'website': 'https://vertel.se',
    'license': 'LGPL-3',
    'category': 'Website/eLearning',
    'depends': ['website_slides'],
    'data': [
        'views/slide_channel_data.xml',
        'data/slide_slides_s1.xml',
        'data/slide_slides_s2.xml',
        'data/slide_slides_s3.xml',
        'data/slide_slides_s4.xml',
        'data/slide_slides_s5.xml',
    ],
    'demo': [
        'demo/slide_slide_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
