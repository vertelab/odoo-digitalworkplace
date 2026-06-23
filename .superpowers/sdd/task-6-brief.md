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
