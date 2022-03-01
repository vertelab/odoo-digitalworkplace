from cgi import test
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class Communication(models.TransientModel):
    _inherit = 'res.config.settings'

    jitsi_url = fields.Char("Jitsi URL", config_parameter='jitsi_url')


    # @api.multi
    #def write(self, vals):
    #    for url in self:
    #        vals = url.jitsi_url.strip("/")
    #        res = super(Communication, self).write(vals)
    #        return res


    # @api.model('jitsi_url')
    # def jitsi_url_modefide (self):
    #     if self.jitsi_url:
    #         modifide = self.jitsi_url.strip("http", "https", "/")
    #         return modifide

    # @api.depends('jitsi_url')

    # def jitsi_url_modefide (self):
    #     for url in self:
    #         if url.jitsi_url:
    #             new_url = url.jitsi_url.replace("http", "https", "/")
    #             _logger.error(f'EYYYOOO{new_url}')
    #             return new_url

    # def set_jitsi_url (self):
    #     for url in self:
    #         _logger.error(f'HEJO2222{url.jitsi_url}')
    #         return url.jitsi_url