import logging

from odoo import models

_logger = logging.getLogger(__name__)


class DavCollection(models.Model):
    _inherit = 'dav.collection'

    def _get_vobject(self, item):
        """Extract the vobject Component from a radicale Item or vobject."""
        if hasattr(item, 'vobject_item'):
            return item.vobject_item
        return item

    def _get_children_dict(self, vobj):
        """Build a name-indexed dict of vobject children."""
        return {c.name.lower(): c for c in vobj.getChildren()}

    def _get_all_children(self, vobj):
        """Get all children including duplicates."""
        return list(vobj.getChildren())

    def from_vobject(self, item):
        result = super().from_vobject(item)
        if self.dav_type == 'addressbook':
            vobj = self._get_vobject(item)
            if vobj.name == 'VCARD':
                children = self._get_children_dict(vobj)
                all_children = self._get_all_children(vobj)
                if 'adr' in children:
                    result.update(self._import_adr(children['adr']))
                if 'org' in children:
                    result.update(self._import_org(children['org']))
                if 'categories' in children:
                    result.update(self._import_categories(children['categories']))
                tel_items = [c for c in all_children if c.name.lower() == 'tel']
                if tel_items:
                    result.update(self._import_tel(tel_items))
        return result

    def to_vobject(self, record):
        vobj = super().to_vobject(record)
        if self.dav_type == 'addressbook':
            n_value = self._export_n(record)
            if n_value:
                vobj.add('n').value = n_value
            tel_items = self._export_tel(record)
            for params, value in tel_items:
                tel = vobj.add('tel')
                tel.value = value
                tel.params = params
            adr_value = self._export_adr(record)
            if adr_value:
                vobj.add('adr').value = adr_value
            org_value = self._export_org(record)
            if org_value:
                vobj.add('org').value = org_value
            categories_value = self._export_categories(record)
            if categories_value:
                vobj.add('categories').value = categories_value
        return vobj

    def _import_adr(self, adr_component):
        self.ensure_one()
        result = {}
        value = adr_component.value
        if isinstance(value, (list, tuple)):
            parts = [str(p or '') for p in value]
        else:
            parts = str(value).split(';')
        parts = [p.strip() for p in parts]
        while len(parts) < 7:
            parts.append('')
        if parts[2]:
            result['street'] = parts[2]
        if parts[1]:
            result['street2'] = parts[1]
        if parts[3]:
            result['city'] = parts[3]
        if parts[4]:
            state = self.env['res.country.state'].search(
                ['|', ('name', '=', parts[4]), ('code', '=', parts[4])],
                limit=1,
            )
            if state:
                result['state_id'] = state.id
        if parts[5]:
            result['zip'] = parts[5]
        if parts[6]:
            country = self.env['res.country'].search(
                ['|', ('name', '=', parts[6]), ('code', '=', parts[6])],
                limit=1,
            )
            if country:
                result['country_id'] = country.id
        return result

    def _import_org(self, org_component):
        self.ensure_one()
        result = {}
        org_name = str(org_component.value).strip()
        if org_name:
            company = self.env['res.partner'].sudo().search([
                ('is_company', '=', True),
                ('name', '=', org_name),
            ], limit=1)
            if not company:
                company = self.env['res.partner'].sudo().create({
                    'name': org_name,
                    'is_company': True,
                })
            result['parent_id'] = company.id
        return result

    def _import_categories(self, cat_component):
        self.ensure_one()
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
                result['category_id'] = [(6, 0, tag_ids)]
        return result

    def _import_tel(self, tel_items):
        self.ensure_one()
        result = {}
        for item in tel_items:
            params = {k.upper(): v for k, v in (item.params or {}).items()}
            tel_types = [t.upper() for t in params.get('TYPE', ['WORK'])]
            value = str(item.value).strip() if item.value else ''
            if not value:
                continue
            if 'CELL' in tel_types:
                result['mobile'] = value
            elif 'phone' not in result or 'WORK' in tel_types:
                result['phone'] = value
        return result

    def _export_n(self, record):
        self.ensure_one()
        name = record.name or ''
        parts = name.strip().split(' ', 1)
        family = parts[0] if parts else name
        given = parts[1].strip() if len(parts) > 1 else ''
        if not family and not given:
            return None
        import vobject
        return vobject.vcard.Name(family=family, given=given)

    def _export_tel(self, record):
        self.ensure_one()
        result = []
        if record.phone:
            result.append(({'TYPE': ['WORK']}, record.phone))
        if record.mobile:
            result.append(({'TYPE': ['CELL']}, record.mobile))
        return result

    def _export_adr(self, record):
        self.ensure_one()
        parts = [''] * 7
        if record.street:
            parts[2] = record.street
        if record.street2:
            parts[1] = record.street2
        if record.city:
            parts[3] = record.city
        if record.state_id:
            parts[4] = record.state_id.name
        if record.zip:
            parts[5] = record.zip
        if record.country_id:
            parts[6] = record.country_id.name
        if not any(parts[1:]):
            return None
        return ';'.join(parts)

    def _export_org(self, record):
        self.ensure_one()
        if record.parent_id:
            return record.parent_id.name
        if record.is_company:
            return record.name
        return None

    def _export_categories(self, record):
        self.ensure_one()
        if record.category_id:
            return ','.join(record.category_id.mapped('name'))
        return None
