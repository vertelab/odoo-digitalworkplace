from odoo.tests import common, tagged


@tagged('post_install', '-at_install')
class TestImmichConfig(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        IrConfigParam = cls.env['ir.config_parameter'].sudo()
        cls.ICP = IrConfigParam

    def test_01_demo_url_set(self):
        """With demo data, immich.url should be set to demo server."""
        self.assertEqual(
            self.ICP.get_param('immich.url'),
            'https://demo.immich.app',
            "Demo URL should be pre-configured",
        )

    def test_02_api_key_not_set(self):
        """API key should NOT be set in demo data (user must obtain their own)."""
        self.assertFalse(
            self.ICP.get_param('immich.api_key'),
            "API key must be obtained from Immich demo instance",
        )

    def test_03_set_and_get_config(self):
        """Setting immich URL and API key should persist."""
        test_url = 'https://photos.example.com'
        test_key = 'test-api-key-12345'

        self.ICP.set_param('immich.url', test_url)
        self.ICP.set_param('immich.api_key', test_key)

        self.assertEqual(self.ICP.get_param('immich.url'), test_url)
        self.assertEqual(self.ICP.get_param('immich.api_key'), test_key)

    def test_04_config_settings_fields(self):
        """ResConfigSettings should have immich fields."""
        config = self.env['res.config.settings'].create({})
        self.assertTrue(hasattr(config, 'immich_url'))
        self.assertTrue(hasattr(config, 'immich_api_key'))

    def test_05_config_settings_persist(self):
        """Setting via res.config.settings should persist."""
        test_url = 'https://photos.example.com'
        test_key = 'test-api-key-12345'

        config = self.env['res.config.settings'].create({
            'immich_url': test_url,
            'immich_api_key': test_key,
        })
        config.execute()

        self.assertEqual(self.ICP.get_param('immich.url'), test_url)
        self.assertEqual(self.ICP.get_param('immich.api_key'), test_key)

    def test_06_attachment_permission(self):
        """ir.attachment should allow /immich/ URLs."""
        attachment = self.env['ir.attachment'].sudo().create({
            'name': 'test_immich_image',
            'url': '/immich/test123/photo',
            'type': 'binary',
            'raw': b'fake-image-data',
        })
        self.assertTrue(attachment._can_bypass_rights_on_media_dialog(
            url='/immich/test123/photo', type='binary'))
