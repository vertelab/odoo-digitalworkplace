# odoo-digitalworkplace — gren 19.0

> **Denna gren är avsiktligt tom.** Modulerna är INTE portade till Odoo 19.
> Grenen finns så att dev-miljöer (`hansolo19`) kan klona den utan att falla,
> men den påstår ingenting om att koden är portad.

## Baseline

| | |
|---|---|
| Källa | `20.0` |
| Moduler | **17** |
| Grenar i repot | `14.0`, `14.0_calendar_voting`, `14.0_videomeeting`, `16.0`, `18.0`, `20.0`, `fix/mail-matrix-appservice`, `main` |

## Moduler

- `calendar_discovery`
- `calendar_mobile_integration`
- `calendar_voting`
- `communication_center_calendar_online_meeting`
- `communication_center_jitsi`
- `communication_center_mail_admin`
- `communication_center_massmail_meeting`
- `communication_center_sip`
- `communication_center_website_event_online_meeting`
- `contact_carddav`
- `digitalworkplace_onboarding`
- `discuss_show_members`
- `mail_matrix`
- `personal_contact_carddav`
- `user_settings_dav`
- `website_immich`
- `website_markdown`

## Blockerare

**1 externa beroenden saknas** i Odoo 19-kärnan och OCA 19.0:

| Beroende | Behövs av |
|---|---|
| `web_editor` | `website_immich` |

### Prioritering

Ett beroende som blockerar många moduler ger mest nytta att lösa först:

- `web_editor` — frisläpper **1** modul(er)

## Nästa steg

Portering sker på `*-pfile`-maskin med versionsagnostisk kod
(`.p.py` / `.p.xml`). Se `/skill:odoo-pfiles`.
