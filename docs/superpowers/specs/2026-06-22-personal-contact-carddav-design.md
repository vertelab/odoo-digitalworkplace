# Personal Contact CardDAV Module

## Purpose

Create `personal_contact_carddav` module that provides a `res.ppartner` model (separate DB table) for user-specific personal contacts, exposed via CardDAV so mobile devices can sync both company-wide contacts (`contact_carddav`) and personal contacts.

## Model: `res.ppartner`

Separate table from `res.partner`. Not an inheritance.

| Field | Type | Notes |
|-------|------|-------|
| `user_id` | M2O `res.users` | `default=lambda self: self.env.user`, `required=True`, `index=True` |
| `name` | Char | required |
| `email` | Char | |
| `phone` | Char | |
| `mobile` | Char | |
| `company_name` | Char | for vCard ORG field |
| `street` | Char | |
| `street2` | Char | |
| `city` | Char | |
| `zip` | Char | |
| `state_id` | M2O `res.country.state` | |
| `country_id` | M2O `res.country` | |
| `notes` | Text | for vCard NOTE |
| `image` | Binary | for vCard PHOTO |
| `category_ids` | M2M `res.partner.category` | for vCard CATEGORIES/tags |

## Security

- Record rule: `[('user_id', '=', user.id)]` — users only see their own contacts
- Model access: full CRUD for all employees (`base.group_user`)

## CardDAV

Single `dav.collection` record with domain `[('user_id', '=', user.id)]` — CardDAV server evaluates per-user dynamically.

Field mappings for vCard:
- `FN` → `name`
- `EMAIL` → `email`
- `TEL` (WORK) → `phone`
- `TEL` (CELL) → `mobile`
- `ORG` → `company_name`
- `ADR` → street/street2/city/zip/state/country
- `PHOTO` → `image`
- `NOTE` → `notes`
- `CATEGORIES` → `category_ids`

Reuses `contact_carddav`'s `dav_collection` vCard import/export methods (ADR, ORG, TEL, CATEGORIES, N) via inheritance.

## Menu

"Personliga Kontakter" after "Kontakter" in the Contacts parent menu.

## Dependencies

- `contact_carddav` (for dav collection vCard methods)
- `contacts` (for menu, categories)

## Data flow

1. Mobile device connects to CardDAV URL for company contacts (`contact_carddav`)
2. Mobile device also connects to CardDAV URL for personal contacts (`personal_contact_carddav`)
3. Personal contacts are only visible to the owning user via record rule and domain filter
