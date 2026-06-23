"""Matrix webhook and .well-known controller for mail_matrix."""

import json
import logging

from odoo import http, _
from odoo.http import request

_logger = logging.getLogger(__name__)


class MailMatrixController(http.Controller):

    @http.route(
        "/.well-known/matrix/server",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def well_known_matrix_server(self):
        """Serve Matrix .well-known delegation.

        Returns the Matrix server domain as configured in settings.
        Coexists with CardDAV/CalDAV/WebDAV on the same Odoo domain.
        """
        matrix_domain = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("mail_matrix.matrix_domain", "")
        )
        if not matrix_domain:
            matrix_domain = request.env["ir.config_parameter"].sudo().get_param(
                "web.base.url", ""
            )
            if matrix_domain:
                # Extract domain from URL
                matrix_domain = matrix_domain.replace("https://", "").replace(
                    "http://", ""
                ).split("/")[0]
                matrix_domain = "matrix." + matrix_domain

        data = {"m.server": f"{matrix_domain}:443"}

        return request.make_response(
            json.dumps(data),
            headers=[
                ("Content-Type", "application/json"),
                ("Access-Control-Allow-Origin", "*"),
            ],
        )

    @http.route(
        "/mail/matrix/webhook",
        type="json",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def matrix_webhook(self, **kw):
        """Receive inbound messages from Matrix via webhook.

        Called by the Matrix server when a message is sent in a
        bridged room. Creates a mail.message in Odoo.

        Auth: validates webhook token stored in system parameters.
        """
        # Validate webhook token
        params = request.jsonrequest or {}
        token = params.get("token", "")
        expected_token = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("mail_matrix.webhook_token", "")
        )

        if expected_token and token != expected_token:
            _logger.warning("Matrix webhook: invalid token")
            return {"status": "error", "message": "Invalid token"}

        # Extract message data
        matrix_room_id = params.get("room_id", "")
        matrix_event_id = params.get("event_id", "")
        matrix_sender = params.get("sender", "")
        body = params.get("body", "")

        if not body:
            return {"status": "ok", "message": "Empty body, skipped"}

        # Find partner by matrix_id
        partner = False
        if matrix_sender:
            partner = (
                request.env["res.partner"]
                .sudo()
                .search([("matrix_id", "=", matrix_sender)], limit=1)
            )

        # Create mail.message (simplified — in production, use mail.thread)
        message_vals = {
            "body": body,
            "subject": f"Matrix: {matrix_sender}",
            "message_type": "comment",
            "subtype_id": request.env.ref("mail.mt_comment").id,
            "is_matrix_message": True,
            "matrix_room_id": matrix_room_id,
            "matrix_event_id": matrix_event_id,
            "matrix_sender_id": matrix_sender,
        }
        if partner:
            message_vals["author_id"] = partner.id

        message = request.env["mail.message"].sudo().create(message_vals)

        _logger.info(
            "Matrix webhook: created message %s from %s in room %s",
            message.id,
            matrix_sender,
            matrix_room_id,
        )

        return {
            "status": "ok",
            "message_id": message.id,
        }
