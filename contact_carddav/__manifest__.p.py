{
    'name': 'Workplace: Contact CardDAV',
    'version': '18.0.1.1.1',
    'summary': 'Exposes res.partner contacts as CardDAV address book.',
    'description': '''
Contact CardDAV
===============

    Exposes res.partner contacts as CardDAV address book.

    Features:

        - Extends Odoo: Builds on dav.collection.
    ''',
    'category': 'Productivity',
    'author': 'Vertel Sverige AB',
    'website': 'https://vertel.se/apps/odoo-digitalworkplace/contact_carddav',
    'license': 'AGPL-3',
    'depends': [
        'contacts',
        'calendar_dav',
    ],
    'data': [
        'data/contact_carddav_data.xml',
    ],
    'external_dependencies': {
        'python': ['vobject'],
    },
    # ------------------------------------------------------------------
    # INSTALLABLE: True — 2026-10-15
    #
    # Spärren 2026-09-22 togs bort sedan den visat sig bygga på en felaktig
    # premiss. Konflikten gäller ENDAST den exakta sökvägen /.well-known/caldav
    # (utan avslutande slash):
    #
    #   /.well-known/caldav/   (med slash)    -> calendar_caldav  307 -> /caldav/
    #   /.well-known/caldav    (utan slash)   -> base_dav        301 -> /.dav
    #
    # DAV-klienter (DAVx5, Thunderbird, iOS) använder formen MED slash, som
    # fortfarande går till calendar_caldav. Båda routes samexisterar.
    #
    # base_dav behövs för CardDAV (/.dav) — dess well-known-routes för
    # carddav/webdav kolliderar inte med något.
    #
    # Verifierat i drift 2026-10-15:
    #   /.well-known/caldav/  -> 307 -> /caldav/        (calendar_caldav)
    #   /.well-known/carddav  -> 301 -> /.dav           (base_dav)
    #   PROPFIND /.dav/       -> 207                    (base_dav/Radicale)
    #
    'installable': True,
    'auto_install': False,
}
