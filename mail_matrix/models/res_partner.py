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

    def _matrix_ensure_bound(self):
        """Return this partner's matrix_id, or the one of its linked user
        (including AI coworkers), or False."""
        self.ensure_one()
        if self.matrix_id:
            return self.matrix_id
        if self.user_ids:
            user = self.user_ids[:1]
            localpart = user._ensure_matrix_localpart(user)
            server = self.env["ir.config_parameter"].sudo().get_param(
                "mail_matrix.server_name", "dms.vertel.se"
            )
            mxid = "@%s:%s" % (localpart, server)
            # Store for future use
            self.write({"matrix_id": mxid})
            return mxid
        return False