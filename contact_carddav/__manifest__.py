{
    'name': 'Workplace: Contact CardDAV',
    'version': '0.1',
    'summary': 'Exposes res.partner contacts as CardDAV address book',
    'category': 'Productivity',
    'author': 'Vertel AB',
    'website': 'https://vertel.se',
    'license': 'AGPL-3',
    'depends': [
        'contacts',
        'base_dav',
        'user_settings_dav',
    ],
    'data': [
        'data/contact_carddav_data.xml',
    ],
    'installable': True,
    'auto_install': False,
}
