# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2025- Vertel AB (<https://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
##############################################################################

"""Core appservice client for mail_matrix (Fas 2).

Handles inbound (transactions from the homeserver to Odoo) and
outbound (Odoo chat messages posted to Matrix rooms) using the
Matrix client-server API with the appservice access token.
"""

import json
import logging

from odoo import api, fields, models, _

from odoo.addons.mail_matrix.publisher.http import matrix_request

_logger = logging.getLogger(__name__)


class MatrixAppservice(models.AbstractModel):
    _name = "matrix.appservice"
    _description = "Matrix Appservice Client"

    # ------------------------------------------------------------------
    # Configuration helpers
    # ------------------------------------------------------------------
    @api.model
    def _get_homeserver_url(self):
        return self.env["ir.config_parameter"].sudo().get_param(
            "mail_matrix.server_url", "https://matrix.dms.vertel.se"
        )

    @api.model
    def _get_as_token(self):
        return self.env["ir.config_parameter"].sudo().get_param(
            "mail_matrix.bot_token", ""
        )

    @api.model
    def _get_hs_token(self):
        return self.env["ir.config_parameter"].sudo().get_param(
            "mail_matrix.hs_token", ""
        )

    @api.model
    def _get_server_name(self):
        return self.env["ir.config_parameter"].sudo().get_param(
            "mail_matrix.server_name", "dms.vertel.se"
        )

    @api.model
    def _is_enabled(self):
        return self.env["ir.config_parameter"].sudo().get_param(
            "mail_matrix.bridge_enabled", False
        )

    # ------------------------------------------------------------------
    # Identity helpers
    # ------------------------------------------------------------------
    @api.model
    def _is_odoo_virtual_user(self, mxid):
        """Echo-protection: True if mxid belongs to this appservice namespace.

        Matches both @odoo_<id> (virtual users) and @odoo-bot (sender localpart).
        """
        server = self._get_server_name()
        if not mxid or not mxid.endswith(":%s" % server):
            return False
        localpart = mxid.split(":", 1)[0].lstrip("@")
        return localpart == "odoo-bot" or localpart.startswith("odoo_")

    @api.model
    def _ensure_virtual_user(self, user):
        """Ensure a virtual Matrix user exists for an Odoo user (incl. AI coworkers).

        Uses the appservice namespace @odoo_<id>:<server>. Creation is done
        through the conduwuit admin console (documented fallback) or the
        registration API; we store the localpart for consistency.
        Returns the full matrix id (or False on failure).
        """
        localpart = user._ensure_matrix_localpart(user)
        server = self._get_server_name()
        mxid = "@%s:%s" % (localpart, server)

        # If partner already has matrix_id — return it
        if user.partner_id.matrix_id:
            return user.partner_id.matrix_id

        # Creation is normally handled out-of-band (admin console / pre-provision).
        # We just record the identity and let the send attempt trigger creation
        # if the homeserver reports M_USER_IN_USE/M_EXCLUSIVE handling below.
        user.partner_id.write({"matrix_id": mxid})
        return mxid

    # ------------------------------------------------------------------
    # Room helpers
    # ------------------------------------------------------------------
    @api.model
    def _find_or_create_dm_room(self, partner, actor_user=False):
        """Return (room_id, binding) for a DM with the given partner.

        Reuses existing binding if present, otherwise creates the room
        via the client-server API as the actor user.
        """
        # Existing binding via partner?
        bindings = self.env["matrix.room.binding"].search(
            [("partner_ids", "in", partner.id), ("is_direct", "=", True)]
        )
        if bindings:
            binding = bindings[:1]
            return binding.room_id, binding

        # Build actor access: if actor_user given, use its matrix id;
        # otherwise fall back to the appservice bot (sender_localpart).
        server = self._get_server_name()
        if actor_user:
            actor_mxid = "@%s:%s" % (actor_user._ensure_matrix_localpart(actor_user), server)
            token = self._get_as_token()  # appservice token can act as ghosts
        else:
            actor_mxid = "@odoo-bot:%s" % server
            token = self._get_as_token()

        partner_mxid = partner.matrix_id or partner._matrix_ensure_bound()
        if not partner_mxid:
            _logger.warning("Partner %s has no matrix_id", partner.name)
            return False, False

        # Create room (appservice can create via client API with as_token)
        payload = {
            "preset": "private_chat",
            "is_direct": True,
            "name": partner.name,
            "invite": [partner_mxid],
        }
        resp = matrix_request(
            self._get_homeserver_url(), "POST", "/_matrix/client/v3/createRoom",
            body=payload, token=token,
        )
        room_id = resp.get("room_id")
        if not room_id:
            _logger.error("createRoom failed: %s", resp)
            return False, False

        binding = self.env["matrix.room.binding"]._get_or_create(
            room_id,
            partner_ids=[partner.id],
            user_ids=[actor_user.id] if actor_user else [],
            is_direct=True,
        )
        _logger.info("Created DM room %s with partner %s", room_id, partner.name)
        return room_id, binding

    # ------------------------------------------------------------------
    # Outbound (Odoo -> Matrix)
    # ------------------------------------------------------------------
    @api.model
    def _post_message(self, channel_id, body, author_id=False):
        """Post a chat message to Matrix.

        channel_id: mail.channel or post id (fallback: use record's thread).
        body: message text.
        author_id: res.users id sending the message (for identity).
        """
        if not self._is_enabled():
            return False

        channel = self.env["discuss.channel"].browse(channel_id)
        if not channel:
            return False

        # Find existing binding or create DM for first partner with matrix_id
        binding = self.env["matrix.room.binding"]._find_by_channel(channel.id)
        if not binding:
            # Look for a partner with matrix_id in the channel
            partners = channel.channel_partner_ids or channel.member_ids
            target = partners.filtered("matrix_id")[:1] or partners[:1]
            if not target:
                return False
            actor = self.env["res.users"].browse(author_id) if author_id else False
            room_id, binding = self._find_or_create_dm_room(target, actor_user=actor)
            if not room_id:
                return False
        else:
            room_id = binding.room_id

        # Determine sender identity
        server = self._get_server_name()
        author = self.env["res.users"].browse(author_id) if author_id else False
        if author:
            author_mxid = "@%s:%s" % (author._ensure_matrix_localpart(author), server)
        else:
            author_mxid = "@odoo-bot:%s" % server

        # Post via client API (appservice can send as ghosts)
        resp = matrix_request(
            self._get_homeserver_url(), "PUT",
            "/_matrix/client/v3/rooms/%s/send/m.room.message/mail_matrix_%s" % (
                matrix_quote(room_id), str(self.env.cr.now).replace(" ", "_")
            ),
            body={"msgtype": "m.text", "body": body},
            token=self._get_as_token(),
        )
        if not resp.get("event_id"):
            _logger.error("send failed: %s", resp)
            return False
        return resp.get("event_id")

    # ------------------------------------------------------------------
    # Inbound (Matrix -> Odoo)
    # ------------------------------------------------------------------
    @api.model
    def _handle_transaction(self, events):
        """Process a batch of events from the homeserver.

        Returns list of created mail.message ids (for tests/logging).
        """
        if not self._is_enabled():
            _logger.debug("mail_matrix disabled — skipping transaction")
            return []

        created = []
        for ev in events:
            ev_type = ev.get("type")
            if ev_type == "m.room.message":
                mid = self._handle_message_event(ev)
                if mid:
                    created.append(mid)
            elif ev_type == "m.room.member":
                # membership/invite — store for potential binding updates
                pass
            # Other event types (create/power_levels/etc.) are ignored
        return created

    @api.model
    def _handle_message_event(self, ev):
        """Create a mail.message for an incoming m.room.message event."""
        sender = ev.get("sender", "")
        room_id = ev.get("room_id", "")
        content = ev.get("content", {}) or {}
        body = content.get("body", "")

        # Echo-protection: skip messages from our own virtual users
        if self._is_odoo_virtual_user(sender):
            _logger.debug("Skipping echo event from %s", sender)
            return False

        if not body:
            return False

        # Find/link an Odoo channel via binding
        binding = self.env["matrix.room.binding"]._find_by_room(room_id)
        if not binding:
            # Unknown room — try to find/create partner by sender and create DM channel
            partner = self.env["res.partner"].search([("matrix_id", "=", sender)], limit=1)
            if not partner:
                # Create a partner record for the external Matrix user
                partner = self._ensure_partner_for_mxid(sender)
            channel = self._ensure_channel_for_partner(partner, room_id)
        else:
            channel = binding.channel_id

        if not channel:
            _logger.warning("No Odoo channel for room %s", room_id)
            return False

        # Find author partner from sender matrix_id (or the created one)
        author = self.env["res.partner"].search([("matrix_id", "=", sender)], limit=1)
        if not author:
            author = self._ensure_partner_for_mxid(sender)

        subtype = self.env.ref("mail.mt_comment", raise_if_not_found=False)

        msg = channel.message_post(
            body=body, message_type="comment",
            subtype_xmlid="mail.mt_comment",
            author_id=author.id if author else False,
        )
        # Attach matrix metadata for traceability
        msg.write({
            "is_matrix_message": True,
            "matrix_room_id": room_id,
            "matrix_event_id": ev.get("event_id", ""),
            "matrix_sender_id": sender,
        })
        _logger.info("Created mail.message %s from %s in %s", msg.id, sender, room_id)
        return msg.id

    @api.model
    def _ensure_partner_for_mxid(self, mxid):
        """Find or create a res.partner for an external Matrix user ID."""
        partner = self.env["res.partner"].search([("matrix_id", "=", mxid)], limit=1)
        if partner:
            return partner
        # Derive a display name from the localpart (before ':')
        localpart = mxid.split(":", 1)[0].lstrip("@")
        partner = self.env["res.partner"].create({
            "name": localpart or mxid,
            "matrix_id": mxid,
        })
        _logger.info("Created partner %s for Matrix user %s", partner.id, mxid)
        return partner

    @api.model
    def _ensure_channel_for_partner(self, partner, room_id):
        """Create/find a Discuss.channel (DM) for a partner and bind it to room."""
        existing = self.env["matrix.room.binding"]._find_by_room(room_id)
        if existing:
            return existing.channel_id
        # Find an existing DM channel with this partner
        channel = self.env["discuss.channel"].search(
            [("channel_type", "=", "chat"), ("channel_partner_ids", "in", [partner.id])],
            limit=1,
        )
        if not channel:
            # Skapa privat chat-kanal (Odoo 18: discuss.channel). Inga group-fält för chat.
            channel = self.env["discuss.channel"].with_context(
                mail_create_nolog=True, mail_create_nosubscribe=True,
            ).create({
                "channel_type": "chat",
                "name": partner.name,
                "channel_partner_ids": [(4, partner.id)],
            })
        self.env["matrix.room.binding"]._get_or_create(room_id, channel_id=channel.id,
                                                       partner_ids=[partner.id], is_direct=True)
        return channel


def matrix_quote(room_id):
    """Minimal URL-quoting for Matrix room IDs (keeps : and alphanumerics)."""
    from urllib.parse import quote as _q
    return _q(room_id, safe="")