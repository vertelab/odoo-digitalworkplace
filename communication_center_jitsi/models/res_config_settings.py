import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class Communication(models.TransientModel):
    _inherit = 'res.config.settings'

    jitsi_url = fields.Char("Jitsi URL", config_parameter='jitsi_url')
