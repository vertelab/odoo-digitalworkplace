from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    immich_url = fields.Char(
        "Immich Server URL",
        config_parameter='immich.url',
        help="URL of your Immich server (e.g. https://photos.example.com)",
    )
    immich_api_key = fields.Char(
        "Immich API Key",
        config_parameter='immich.api_key',
        help="API key from your Immich account settings",
    )
