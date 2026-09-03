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

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class MatrixRoomBinding(models.Model):
    """Mapping between a Matrix room and an Odoo Discuss.channel (DM or channel)."""

    _name = "matrix.room.binding"
    _description = "Matrix Room Binding"

    room_id = fields.Char(
        string="Matrix Room ID",
        required=True,
        index=True,
        copy=False,
    )
    channel_id = fields.Many2one(
        "discuss.channel",
        string="Odoo Channel",
        ondelete="cascade",
        index=True,
    )
    # Partners/users with Matrix identity involved in this room.
    partner_ids = fields.Many2many(
        "res.partner",
        string="Partners",
        help="Partners with Matrix identity in this room.",
    )
    user_ids = fields.Many2many(
        "res.users",
        string="Users",
        help="Odoo users (including AI coworkers) in this room.",
    )
    is_direct = fields.Boolean(
        string="Is Direct Message",
        default=True,
        help="True for DM rooms, False for group/channel rooms.",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )

    _sql_constraints = [
        ("room_id_uniq", "UNIQUE(room_id)", "Matrix room already bound."),
    ]

    @api.model
    def _get_or_create(self, room_id, channel_id=None, partner_ids=None,
                       user_ids=None, is_direct=True):
        """Return existing binding for room_id or create a new one."""
        binding = self.search([("room_id", "=", room_id)], limit=1)
        if binding:
            return binding
        vals = {
            "room_id": room_id,
            "is_direct": is_direct,
        }
        if channel_id:
            vals["channel_id"] = channel_id
        if partner_ids:
            vals["partner_ids"] = [(6, 0, partner_ids)]
        if user_ids:
            vals["user_ids"] = [(6, 0, user_ids)]
        return self.create(vals)

    @api.model
    def _find_by_channel(self, channel_id):
        """Return binding for a given Odoo channel, if any."""
        return self.search([("channel_id", "=", channel_id)], limit=1)

    @api.model
    def _find_by_room(self, room_id):
        """Return binding for a given Matrix room."""
        return self.search([("room_id", "=", room_id)], limit=1)