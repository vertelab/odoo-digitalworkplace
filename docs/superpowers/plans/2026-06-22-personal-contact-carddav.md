# Personal Contact CardDAV Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create `personal_contact_carddav` Odoo module with `res.ppartner` model for user-specific personal contacts, exposed via CardDAV.

**Architecture:** New module with separate `res.ppartner` DB table. Single `dav.collection` record with dynamic domain `[('user_id', '=', user.id)]`. vCard import/export reuses `contact_carddav` methods with overridden ORG handling for `company_name`.

**Tech Stack:** Odoo 18, base_dav (CardDAV), vobject

## Global Constraints

- Module location: `/usr/share/odoo-digitalworkplace/personal_contact_carddav/`
- Dependencies: `contact_carddav`, `contacts`
- Model name: `res.ppartner` (separate table, no `_inherit` from `res.partner`)
- CardDAV domain: `[('user_id', '=', user.id)]`
- Record rule: `[('user_id', '=', user.id)]`
- Menu: "Personliga Kontakter" under `menu_contacts` with `sequence=3`

---
### Task 1: Module scaffold + manifest

**Files:**
- Create: `personal_contact_carddav/__init__.py`
- Create: `personal_contact_carddav/__manifest__.py`
- Create: `personal_contact_carddav/models/__init__.py`
- Create: `personal_contact_carddav/security/ir.model.access.csv`

- [ ] **Step 1: Create `__init__.py`**

```python
from . import models
```

- [ ] **Step 2: Create `__manifest__.py`**

```python
{
    'name': 'Personal Contact CardDAV',
    'version': '0.1',
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
        'views/res_ppartner_views.xml',
        'data/personal_contact_carddav_data.xml',
    ],
    'installable': True,
    'auto_install': False,
}
```

- [ ] **Step 3: Create `models/__init__.py`**

```python
from . import res_ppartner
from . import dav_collection
```

- [ ] **Step 4: Create `security/ir.model.access.csv`**

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_res_ppartner_user,res.ppartner.user,model_res_ppartner,base.group_user,1,1,1,1
```

---
### Task 2: `res.ppartner` model

**Files:**
- Create: `personal_contact_carddav/models/res_ppartner.py`

- [ ] **Step 1: Create model**

```python
from odoo import models, fields, api


class ResPpartner(models.Model):
    _name = 'res.ppartner'
    _description = 'Personal Partner'
    _order = 'name'
    _rec_name = 'name'
    _check_company_auto = False

    user_id = fields.Many2one(
        'res.users',
        string='User',
        required=True,
        index=True,
        default=lambda self: self.env.user,
    )
    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')
    company_name = fields.Char(string='Company')
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street2')
    city = fields.Char(string='City')
    zip = fields.Char(string='ZIP')
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')
    notes = fields.Text(string='Notes')
    image = fields.Binary(string='Image', attachment=True)
    category_ids = fields.Many2many(
        'res.partner.category',
        'res_ppartner_category_rel',
        'ppartner_id',
        'category_id',
        string='Tags',
    )
```

- [ ] **Step 2: Verify file**

---
### Task 3: `dav.collection` inheritance for ppartner vCard

**Files:**
- Create: `personal_contact_carddav/models/dav_collection.py`

- [ ] **Step 1: Create dav_collection.py**

`contact_carddav`'s `from_vobject` maps ORG → `parent_id` (relation to `res.partner`). For `res.ppartner`, ORG must map to `company_name` (Char). Override `from_vobject` and `to_vobject` to handle ppartner collections.

```python
import logging

from odoo import models

_logger = logging.getLogger(__name__)


class DavCollection(models.Model):
    _inherit = 'dav.collection'

    def _get_vobject(self, item):
        if hasattr(item, 'vobject_item'):
            return item.vobject_item
        return item

    def _get_children_dict(self, vobj):
        return {c.name.lower(): c for c in vobj.getChildren()}

    def from_vobject(self, item):
        result = super().from_vobject(item)
        if self.dav_type == 'addressbook' and self.model_id.model == 'res.ppartner':
            vobj = self._get_vobject(item)
            if vobj.name == 'VCARD':
                children = self._get_children_dict(vobj)
                if 'org' in children:
                    if 'parent_id' in result:
                        del result['parent_id']
                    org_name = str(children['org'].value).strip()
                    if org_name:
                        result['company_name'] = org_name
        return result

    def to_vobject(self, record):
        vobj = super().to_vobject(record)
        if self.dav_type == 'addressbook' and self.model_id.model == 'res.ppartner':
            if record.company_name:
                vobj.add('org').value = record.company_name
        return vobj
```

- [ ] **Step 2: Verify file**

---
### Task 4: Views and menu

**Files:**
- Create: `personal_contact_carddav/views/res_ppartner_views.xml`

- [ ] **Step 1: Create views XML**

Menu "Personliga Kontakter" placed after "Kontakter" under `menu_contacts` with `sequence=3`.

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="action_personal_contacts" model="ir.actions.act_window">
        <field name="name">Personliga Kontakter</field>
        <field name="res_model">res.ppartner</field>
        <field name="view_mode">list,form</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Skapa en personlig kontakt
            </p>
        </field>
    </record>

    <record id="view_res_ppartner_list" model="ir.ui.view">
        <field name="name">res.ppartner.list</field>
        <field name="model">res.ppartner</field>
        <field name="arch" type="xml">
            <list string="Personliga Kontakter">
                <field name="name"/>
                <field name="email"/>
                <field name="phone"/>
                <field name="mobile"/>
                <field name="company_name"/>
            </list>
        </field>
    </record>

    <record id="view_res_ppartner_form" model="ir.ui.view">
        <field name="name">res.ppartner.form</field>
        <field name="model">res.ppartner</field>
        <field name="arch" type="xml">
            <form string="Personlig Kontakt">
                <sheet>
                    <field name="image" widget="image" class="oe_avatar"/>
                    <div class="oe_title">
                        <h1><field name="name" placeholder="Namn..."/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="email" widget="email"/>
                            <field name="phone" widget="phone"/>
                            <field name="mobile" widget="phone"/>
                            <field name="company_name"/>
                        </group>
                        <group>
                            <field name="street" placeholder="Gata..."/>
                            <field name="street2"/>
                            <field name="city"/>
                            <field name="zip"/>
                            <field name="state_id" options="{'no_create': True}"/>
                            <field name="country_id" options="{'no_create': True}"/>
                        </group>
                    </group>
                    <group string="Tags">
                        <field name="category_ids" widget="many2many_tags"/>
                    </group>
                    <notebook>
                        <page string="Anteckningar">
                            <field name="notes"/>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_res_ppartner_search" model="ir.ui.view">
        <field name="name">res.ppartner.search</field>
        <field name="model">res.ppartner</field>
        <field name="arch" type="xml">
            <search string="Sök personliga kontakter">
                <field name="name"/>
                <field name="email"/>
                <field name="phone"/>
                <field name="mobile"/>
                <field name="company_name"/>
            </search>
        </field>
    </record>

    <menuitem id="menu_personal_contacts"
        name="Personliga Kontakter"
        parent="menu_contacts"
        sequence="3"
        action="action_personal_contacts"
        groups="base.group_user"/>
</odoo>
```

- [ ] **Step 2: Verify XML file**

---
### Task 5: CardDAV data — collection + field mappings

**Files:**
- Create: `personal_contact_carddav/data/personal_contact_carddav_data.xml`

- [ ] **Step 1: Create data XML**

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="collection_personal_contacts" model="dav.collection">
        <field name="name">Personliga Kontakter</field>
        <field name="dav_type">addressbook</field>
        <field name="model_id" ref="model_res_ppartner"/>
        <field name="domain">[('user_id', '=', user.id)]</field>
        <field name="rights">authenticated</field>
    </record>

    <record id="field_mapping_ppartner_fn" model="dav.collection.field_mapping">
        <field name="name">FN</field>
        <field name="field_id" ref="field_res_ppartner__name"/>
        <field name="collection_id" ref="collection_personal_contacts"/>
    </record>

    <record id="field_mapping_ppartner_email" model="dav.collection.field_mapping">
        <field name="name">EMAIL</field>
        <field name="field_id" ref="field_res_ppartner__email"/>
        <field name="collection_id" ref="collection_personal_contacts"/>
    </record>

    <record id="field_mapping_ppartner_photo" model="dav.collection.field_mapping">
        <field name="name">PHOTO</field>
        <field name="field_id" ref="field_res_ppartner__image"/>
        <field name="collection_id" ref="collection_personal_contacts"/>
    </record>

    <record id="field_mapping_ppartner_note" model="dav.collection.field_mapping">
        <field name="name">NOTE</field>
        <field name="field_id" ref="field_res_ppartner__notes"/>
        <field name="collection_id" ref="collection_personal_contacts"/>
    </record>
</odoo>
```

- [ ] **Step 2: Generate external IDs for field refs**

The field refs like `field_res_ppartner__name` may not resolve until the module is installed. Verify that Odoo auto-generates these external IDs from the model fields. If not, use `ir.model.fields` search or explicit noupdate records.

Alternative approach for field references (if auto-generated refs fail):

```xml
<record id="field_mapping_ppartner_fn" model="dav.collection.field_mapping">
    <field name="name">FN</field>
    <field name="field_id" search="[('model_id.model', '=', 'res.ppartner'), ('name', '=', 'name')]"/>
    <field name="collection_id" ref="collection_personal_contacts"/>
</record>
```

Use `search` attribute instead of `ref` if auto-generated `field_res_ppartner__*` external IDs are not available at data file load time.

- [ ] **Step 3: Verify XML**

---
### Task 6: Record rule for user isolation

**Files:**
- Modify: `personal_contact_carddav/security/ir.model.access.csv` (add record rule)

- [ ] **Step 1: Add record rule to `ir.model.access.csv`**

The CSV already has model access. Add record rule via an XML data file instead:

Create `personal_contact_carddav/security/res_ppartner_security.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="rule_res_ppartner_user" model="ir.rule">
        <field name="name">res.ppartner: own records only</field>
        <field name="model_id" ref="model_res_ppartner"/>
        <field name="global" eval="True"/>
        <field name="domain_force">[('user_id', '=', user.id)]</field>
    </record>
</odoo>
```

- [ ] **Step 2: Add security XML to manifest data**

Add `'security/res_ppartner_security.xml',` to `__manifest__.py` data list (before the other data entries).

---
### Task 7: Tests

**Files:**
- Create: `personal_contact_carddav/tests/__init__.py`
- Create: `personal_contact_carddav/tests/test_res_ppartner.py`

- [ ] **Step 1: Create `tests/__init__.py`**

```python
from . import test_res_ppartner
```

- [ ] **Step 2: Create test file**

```python
from odoo.tests import common, tagged


@tagged('-at_install', 'post_install')
class TestResPpartner(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Ppartner = cls.env['res.ppartner']
        cls.user = cls.env.user
        cls.other_user = cls.env['res.users'].create({
            'name': 'Test User 2',
            'login': 'testuser2',
        })

    def test_create_with_default_user(self):
        record = self.Ppartner.create({
            'name': 'Test Contact',
        })
        self.assertEqual(record.user_id, self.user)

    def test_create_with_explicit_user(self):
        record = self.Ppartner.create({
            'name': 'Other Contact',
            'user_id': self.other_user.id,
        })
        self.assertEqual(record.user_id, self.other_user)

    def test_record_rule_filters_by_user(self):
        self.Ppartner.create({'name': 'My Contact'})
        self.Ppartner.with_user(self.other_user).create({'name': 'Other Contact'})

        my_records = self.Ppartner.search([])
        self.assertIn('My Contact', my_records.mapped('name'))
        self.assertNotIn('Other Contact', my_records.mapped('name'))

    def test_search_all_fields(self):
        record = self.Ppartner.create({
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '123456789',
            'mobile': '987654321',
            'company_name': 'ACME Corp',
        })
        self.assertEqual(record.name, 'John Doe')
        self.assertEqual(record.email, 'john@example.com')
        self.assertEqual(record.company_name, 'ACME Corp')
```
