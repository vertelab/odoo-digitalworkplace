from odoo import api, models, fields
import logging
 
_logger = logging.Logger('.........')

class TestingButton(models.Model):
    _inherit = 'res.users'

    def cancel_tours(self):
        _logger.warning("hello")