import json
import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class MailMessage(models.Model):
    _inherit = "mail.message"

    matrix_room_id = fields.Char(
        string="Matrix Room ID",
        copy=False,
    )
    matrix_event_id = fields.Char(
        string="Matrix Event ID",
        copy=False,
    )
    matrix_sender_id = fields.Char(
        string="Matrix Sender ID",
        copy=False,
    )
    is_matrix_message = fields.Boolean(
        string="Is Matrix Message",
        default=False,
        copy=False,
    )

    def _matrix_publish(self):
        """Publish this message to Matrix via the appservice client.

        Returns True if at least one Matrix recipient was targeted.
        """
        self.ensure_one()

        # Find matrix recipients: partners with matrix_id, or users with matrix identity
        partner_ids = self.partner_ids or self.mapped(
            "notification_ids.res_partner_id"
        )
        matrix_partners = partner_ids.filtered(
            lambda p: p.matrix_id or p.user_ids
        )
        if not matrix_partners:
            _logger.debug("No Matrix recipients for message %s", self.id)
            return False

        # Determine the thread: if this message is in a mail.channel, use it.
        channel = False
        if self.model == "discuss.channel":
            channel = self.env["discuss.channel"].browse(self.res_id)

        author_id = self.author_id.id if self.author_id else False

        outbound = self.env["matrix.appservice"]
        if channel:
            # Post to the bound Matrix room for this channel
            return outbound._post_message(channel.id, self.body or "", author_id=author_id)
        else:
            # For non-channel messages, send DM to each matrix partner
            ok = True
            for partner in matrix_partners:
                m = self.env["matrix.appservice"]
                room_id, binding = m._find_or_create_dm_room(partner)
                if room_id:
                    resp = self.env["matrix.appservice"]._post_message(
                        binding.channel_id.id if binding else False,
                        self.body or "",
                        author_id=author_id,
                    )
                    ok = ok and bool(resp)
            return ok