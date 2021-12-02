from odoo import models, fields, api, _


class Communication(models.TransientModel):
    _inherit = 'res.config.settings'

    jitsi_url = fields.Char("Jitsi URL", config_parameter='jitsi_url', default='')
