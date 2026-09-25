{
    'name': 'Personal Contact CardDAV',
    'version': '18.0.1.0.0',
    'summary': 'User-specific personal contacts exposed as CardDAV address book.',
    'description': '''
Personal Contact CardDAV
========================

    User-specific personal contacts exposed as CardDAV address book.

    Features:

        - UI Integration: Extends 1 view(s) in the Odoo interface.
        - Extends Odoo: Builds on dav.collection, name.
    ''',
    'category': 'Productivity',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-digitalworkplace/personal_contact_carddav',
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
