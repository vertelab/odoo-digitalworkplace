{
    'name': 'Workplace: Contact CardDAV',
    'version': '0.1',
    'summary': 'Exposes res.partner contacts as CardDAV address book',
    'category': 'Productivity',
    'author': 'Vertel Sverige AB',
    'website': 'https://vertel.se',
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
    # INSTALLABLE: False — 2026-09-22
    #
    # Ingår i OCA/Radicale-sparet (base_dav), som spärrats till förmån för
    # Vertels egna calendar_caldav (endpoint /caldav/). Båda registrerar
    # /.well-known/caldav och kolliderar — bara ett får vara installerat.
    # Se README "CalDAV: val av spår".
    #
    'installable': True,
    'auto_install': False,
}
