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
