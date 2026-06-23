{
    'name': 'Personal Contact CardDAV',
    'version': '18.0.1.0.0',
    'summary': 'User-specific personal contacts exposed as CardDAV address book',
    'category': 'Productivity',
    'author': 'Vertel AB',
    'website': 'https://vertel.se',
    'license': 'AGPL-3',
    'depends': [
        'contacts',
        'contact_carddav',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/res_ppartner_security.xml',
        'views/res_ppartner_views.xml',
        'data/personal_contact_carddav_data.xml',
    ],
    'installable': True,
    'auto_install': False,
}
