# odoo-digitalworkplace

## Porteringsstatus

18.0 är baseline. 19.0/20.0 visar om p-filen har ett villkor för utgåvan
— inte om grenen finns. Blockerare är `depends` som saknas i 20.0
(kärna + alla 20.0-grenar).

| Modul | Beskrivning | Manifest | p-fil | 19.0 | 20.0 | Blockerare |
|---|---|---|---|---|---|---|
| calendar_discovery | Sets up an endpoint that redirects CalDAV/CardCAV to the ... | 1.0.0 | 0 | — | — | — |
| calendar_mobile_integration | Syncs the Odoo calendar with other apps. | 1.0.0 | 0 | — | — | — |
| calendar_voting | Ability to vote for which day a meeting in Odoo should be... | 1.0.1 | 1 | — | ✓ | — |
| communication_center_calendar_online_meeting | Setup a link for your online meeting. | 1.0.0 | 0 | — | — | — |
| communication_center_jitsi | Setup communication with Jitsi. | 1.0.0 | 0 | — | — | — |
| communication_center_mail_admin | Edit and Delete option for chatters Message & Log Note.s ... | 1.0.1 | 1 | — | ✓ | — |
| communication_center_massmail_meeting | Setup Jitsi for Mass Mailing. | 1.0.0 | 0 | — | — | — |
| communication_center_sip | Make calls using a VOIP system. | 1.0.1 | 1 | — | ✓ | — |
| communication_center_website_event_online_meeting | Setup a link for your online event. | 1.0.0 | 0 | — | — | — |
| contact_carddav | Exposes res.partner contacts as CardDAV address book. | 1.0.0 | 0 | — | — | — |
| digitalworkplace_onboarding | Onboardingskurs: chatt (Matrix) och web-möte (Jitsi) | 1.0.0 | 0 | — | — | — |
| discuss_show_members | Show Discuss Members. | 1.0.0 | 1 | — | ✓ | — |
| mail_matrix | Bridge Odoo mail/chat with Matrix protocol via RabbitMQ. | 0.0.5 | 1 | — | ✓ | — |
| personal_contact_carddav | User-specific personal contacts exposed as CardDAV addres... | 1.0.0 | 3 | ✓ | ✓ | — |
| user_settings_dav | Adds CalDAV/CardDAV settings for users. | 1.0.0 | 0 | — | — | — |
| website_immich | Find images from your Immich server. | 1.0.0 | 0 | — | — | `web_editor` |
| website_markdown | Renders Markdown content on the website. | 1.0.0 | 0 | — | — | — |
