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
