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
