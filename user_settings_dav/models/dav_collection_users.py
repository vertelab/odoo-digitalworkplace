import logging
from odoo import models, fields

_logger = logging.getLogger("\033[100m"+__name__+"\033[0m")

class DavCollectionUsers (models.Model):
    _inherit = "res.users"

    dav_collection_ids = fields.Many2many(comodel_name="dav.collection")

