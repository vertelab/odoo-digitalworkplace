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
