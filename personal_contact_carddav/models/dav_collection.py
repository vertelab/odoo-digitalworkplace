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

    def _export_org(self, record):
        if self.model_id.model == 'res.ppartner':
            return None
        return super()._export_org(record)

    def _export_categories(self, record):
        if self.model_id.model == 'res.ppartner':
            if record.category_ids:
                return ','.join(record.category_ids.mapped('name'))
            return None
        return super()._export_categories(record)

    def _import_org(self, org_component):
        self.ensure_one()
        if self.model_id.model == 'res.ppartner':
            result = {}
            org_name = str(org_component.value).strip()
            if org_name:
                result['company_name'] = org_name
            return result
        return super()._import_org(org_component)

    def _import_categories(self, cat_component):
        self.ensure_one()
        if self.model_id.model != 'res.ppartner':
            return super()._import_categories(cat_component)
        result = {}
        cat_string = str(cat_component.value).strip()
        if cat_string:
            tag_names = [t.strip() for t in cat_string.split(',') if t.strip()]
            tag_ids = []
            for tag_name in tag_names:
                tag = self.env['res.partner.category'].sudo().search(
                    [('name', '=', tag_name)], limit=1)
                if not tag:
                    tag = self.env['res.partner.category'].sudo().create({
                        'name': tag_name,
                    })
                tag_ids.append(tag.id)
            if tag_ids:
                result['category_ids'] = [(6, 0, tag_ids)]
        return result

    def from_vobject(self, item):
        result = super().from_vobject(item)
        if self.dav_type == 'addressbook' and self.model_id.model == 'res.ppartner':
            vobj = self._get_vobject(item)
            if vobj.name == 'VCARD':
                children = self._get_children_dict(vobj)
                if 'org' in children:
                    if 'parent_id' in result:
                        del result['parent_id']
        return result

    def to_vobject(self, record):
        vobj = super().to_vobject(record)
        if self.dav_type == 'addressbook' and self.model_id.model == 'res.ppartner':
            if record.company_name:
                vobj.add('org').value = record.company_name
        return vobj
