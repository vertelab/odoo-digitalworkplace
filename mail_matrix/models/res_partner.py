import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    matrix_id = fields.Char(
        string="Matrix ID",
        help="Matrix user ID (e.g. @username:server). Used for Matrix messaging routing.",
        copy=False,
    )
