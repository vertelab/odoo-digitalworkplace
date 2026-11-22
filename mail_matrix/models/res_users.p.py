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


class ResUsers(models.Model):
    _inherit = "res.users"

    matrix_localpart = fields.Char(
        string="Matrix Localpart",
        help="Local part of the virtual Matrix user for this Odoo user "
             "(e.g. 'odoo_5' → @odoo_5:server). Created on demand.",
        copy=False,
        index=True,
    )

    @api.model
    def _ensure_matrix_localpart(self, user):
        """Ensure a consistent matrix localpart for an Odoo user (incl. AI coworkers).

        Returns the localpart string (without @server).
        """
        if user.matrix_localpart:
            return user.matrix_localpart
        localpart = "odoo_%s" % user.id
        user.write({"matrix_localpart": localpart})
        return localpart