import base64

import vobject

from odoo.tests import common, tagged

# A 1x1 transparent PNG, small enough to keep the test fast.
PNG_1PX = base64.b64decode(
    b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk'
    b'YPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='
)


@tagged('-at_install', 'post_install')
class TestDavSerialization(common.TransactionCase):
    """Round-trip tests for the Personal Contacts address book.

    Both bugs covered here were silent: the collection answered PROPFIND
    fine and only broke on the properties that carry binary or list data.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.collection = cls.env.ref(
            'personal_contact_carddav.collection_personal_contacts')
        cls.Ppartner = cls.env['res.ppartner']

    def _vcard(self, record):
        return self.collection.to_vobject(record)

    def _child(self, vobj, name):
        for child in vobj.getChildren():
            if child.name.lower() == name:
                return child
        return None

    def test_photo_export_is_base64_string(self):
        """PHOTO must serialize; base_dav used to call str.decode()."""
        record = self.Ppartner.create({
            'name': 'Photo Person',
            'image': base64.b64encode(PNG_1PX),
        })
        vobj = self._vcard(record)
        photo = self._child(vobj, 'photo')
        self.assertTrue(photo, 'PHOTO property missing from the vCard')
        self.assertEqual(base64.b64decode(photo.value), PNG_1PX)

        # serialize() is where the old code raised AttributeError.
        text = vobj.serialize()
        self.assertIn('PHOTO', text)

    def test_photo_import_is_base64_string(self):
        """A client sending PHOTO;ENCODING=b must not crash the import."""
        card = vobject.readOne(
            'BEGIN:VCARD\r\n'
            'VERSION:3.0\r\n'
            'FN:Imported Person\r\n'
            'PHOTO;ENCODING=b;TYPE=PNG:%s\r\n'
            'END:VCARD\r\n' % base64.b64encode(PNG_1PX).decode()
        )
        values = self.collection.from_vobject(card)
        self.assertIn('image', values)
        self.assertEqual(base64.b64decode(values['image']), PNG_1PX)

    def test_photo_round_trip(self):
        record = self.Ppartner.create({
            'name': 'Round Trip',
            'image': base64.b64encode(PNG_1PX),
        })
        exported = self._vcard(record).serialize()
        values = self.collection.from_vobject(vobject.readOne(exported))
        self.assertEqual(base64.b64decode(values['image']), PNG_1PX)

    def test_categories_export_is_a_list(self):
        """CATEGORIES is a list in vCard 3.0.

        Passing a comma-joined string made vobject escape every comma
        ("A\\,,B"), so clients saw one tag literally named "A,B".
        """
        tag_a = self.env['res.partner.category'].create({'name': 'Family'})
        tag_b = self.env['res.partner.category'].create({'name': 'Work'})
        record = self.Ppartner.create({
            'name': 'Tagged Person',
            'category_ids': [(6, 0, (tag_a | tag_b).ids)],
        })
        categories = self._child(self._vcard(record), 'categories')
        self.assertTrue(categories, 'CATEGORIES property missing')
        self.assertEqual(sorted(categories.value), ['Family', 'Work'])

        line = [
            ln for ln in self._vcard(record).serialize().splitlines()
            if ln.startswith('CATEGORIES')
        ][0]
        self.assertNotIn('\\,', line, 'commas must not be escaped')

    def test_categories_import(self):
        card = vobject.readOne(
            'BEGIN:VCARD\r\n'
            'VERSION:3.0\r\n'
            'FN:Tagged Import\r\n'
            'CATEGORIES:Family,Work\r\n'
            'END:VCARD\r\n'
        )
        values = self.collection.from_vobject(card)
        self.assertIn('category_ids', values)
        names = self.env['res.partner.category'].browse(
            values['category_ids'][0][2]).mapped('name')
        self.assertEqual(sorted(names), ['Family', 'Work'])

    def test_company_name_stays_local(self):
        """ORG must land in company_name, never create a res.partner."""
        card = vobject.readOne(
            'BEGIN:VCARD\r\n'
            'VERSION:3.0\r\n'
            'FN:Consultant\r\n'
            'ORG:Some Customer AB\r\n'
            'END:VCARD\r\n'
        )
        values = self.collection.from_vobject(card)
        self.assertEqual(values.get('company_name'), 'Some Customer AB')
        self.assertNotIn('parent_id', values)

        leaked = self.env['res.partner'].search([
            ('name', '=', 'Some Customer AB'),
        ])
        self.assertFalse(leaked, 'ORG must not create a shared res.partner')
