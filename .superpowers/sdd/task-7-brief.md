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
