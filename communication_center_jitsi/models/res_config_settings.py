import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class Communication(models.TransientModel):
    _inherit = 'res.config.settings'

    jitsi_url = fields.Char("Jitsi URL", config_parameter='jitsi_url')
    jitsi_app_id = fields.Char(string="Jitsi App ID", config_parameter='jitsi_app_id')
    jwt_secret = fields.Char(string="Jitsi Configuration JWT secret", config_parameter='jwt_secret')
