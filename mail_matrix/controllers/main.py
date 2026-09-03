"""Matrix controller for mail_matrix (Fas 2).

- /.well-known/matrix/server — federation delegation
- /mail/matrix/appservice — appservice transaction endpoint (inbound)
- /mail/matrix/webhook — legacy webhook (retained until fully phased out)
"""

import json
import logging

from odoo import http, _
from odoo.http import request

from odoo.addons.mail_matrix.publisher.http import matrix_request

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
        """Serve Matrix .well-known delegation."""
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
                matrix_domain = matrix_domain.replace("https://", "").replace(
                    "http://", ""
                ).split("/")[0]

        data = {"m.server": f"{matrix_domain}:443"}
        return request.make_response(
            json.dumps(data),
            headers=[
                ("Content-Type", "application/json"),
                ("Access-Control-Allow-Origin", "*"),
            ],
        )

    @http.route(
        "/mail/matrix/appservice",
        type="http",
        auth="public",
        methods=["PUT", "POST"],
        csrf=False,
        save_session=False,
    )
    def appservice_transaction(self, **kw):
        """Receive appservice transactions from the homeserver.

        Legacy alias (kept for compatibility). The canonical appservice path
        is /_matrix/app/v1/transactions/<txn_id> (see below).
        """
        return self._handle_transaction()

    @http.route(
        "/_matrix/app/v1/transactions/<txn_id>",
        type="http",
        auth="public",
        methods=["PUT", "POST"],
        csrf=False,
        save_session=False,
    )
    def appservice_transaction_v1(self, txn_id, **kw):
        """Receive appservice transactions from the homeserver (canonical path)."""
        _logger.info("Appservice transaction %s", txn_id)
        return self._handle_transaction()

    def _handle_transaction(self):
        """Shared appservice transaction handler."""
        # Appservice protocol: Authorization: Bearer <hs_token>
        auth_header = request.httprequest.headers.get("Authorization", "")
        expected = request.env["ir.config_parameter"].sudo().get_param(
            "mail_matrix.hs_token", ""
        )
        if expected and auth_header != "Bearer %s" % expected:
            _logger.warning("Appservice: invalid hs_token in Authorization")
            return self._as_response(403, {"errcode": "M_FORBIDDEN", "error": "Invalid hs_token"})

        # Read raw body
        try:
            body = request.httprequest.get_data(as_text=True)
            data = json.loads(body or "{}")
        except Exception as e:
            _logger.error("Appservice: bad JSON: %s", e)
            return self._as_response(400, {"errcode": "M_BAD_JSON", "error": "Bad JSON"})

        events = data.get("events", [])
        _logger.info("Appservice transaction with %d events", len(events))

        try:
            created = request.env["matrix.appservice"].sudo()._handle_transaction(events)
        except Exception:
            _logger.exception("Appservice transaction processing failed")
            created = []

        # Matrix appservice protocol: always 200 for accepted transactions.
        return self._as_response(200, {"status": "ok", "created": len(created)})

    def _as_response(self, code, payload):
        body = json.dumps(payload)
        return request.make_response(
            body,
            headers=[("Content-Type", "application/json")],
            status=code,
        )

    @http.route(
        "/mail/matrix/webhook",
        type="json",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def matrix_webhook(self, **kw):
        """Legacy webhook endpoint (retained for compatibility)."""
        try:
            data = request.jsonrequest
        except AttributeError:
            data = request.get_json_data() if hasattr(request, "get_json_data") else {}
        if not data:
            data = kw

        token = data.get("token", "")
        expected_token = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("mail_matrix.webhook_token", "")
        )
        if expected_token and token != expected_token:
            _logger.warning("Matrix webhook: invalid token")
            return {"status": "error", "message": "Invalid token"}

        sender = data.get("sender", "")
        body = data.get("body", "")
        room_id = data.get("room_id", "")
        if not body:
            return {"status": "ok", "message": "Empty body"}

        # Delegate to appservice handler (reuse logic; webhook payload maps to event)
        event = {
            "type": "m.room.message",
            "sender": sender,
            "room_id": room_id,
            "content": {"body": body},
            "event_id": data.get("event_id", ""),
        }
        created = request.env["matrix.appservice"].sudo()._handle_transaction([event])
        return {"status": "ok", "message_id": created[0] if created else 0}