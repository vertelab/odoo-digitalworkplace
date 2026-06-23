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
        """Publish this message to RabbitMQ for Matrix routing."""
        self.ensure_one()

        partner_ids = self.partner_ids or self.mapped(
            "notification_ids.res_partner_id"
        )
        matrix_recipients = partner_ids.filtered(
            lambda p: p.matrix_id
        ).mapped("matrix_id")

        matrix_sender = ""
        if self.author_id and self.author_id.matrix_id:
            matrix_sender = self.author_id.matrix_id

        if not matrix_recipients:
            _logger.debug("No Matrix recipients for message %s", self.id)
            return False

        payload = {
            "message_id": self.id,
            "model": self.model,
            "res_id": self.res_id,
            "body": self.body or "",
            "subject": self.subject or "",
            "date": self.date.isoformat() if self.date else "",
            "author_id": self.author_id.id if self.author_id else 0,
            "matrix_sender": matrix_sender,
            "matrix_recipients": list(matrix_recipients),
            "record_name": self.record_name or "",
        }

        try:
            from odoo.addons.mail_matrix.publisher.matrix_publisher import publish_message
            publish_message(payload)
            _logger.info("Published message %s to Matrix via RabbitMQ", self.id)
            return True
        except Exception as e:
            _logger.error("Failed to publish message %s: %s", self.id, e)
            return False
