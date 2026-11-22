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


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    mail_matrix_bridge_enabled = fields.Boolean(
        string="Matrix Bridge Enabled",
        config_parameter="mail_matrix.bridge_enabled",
        default=False,
    )
    mail_matrix_server_name = fields.Char(
        string="Matrix Server Name",
        config_parameter="mail_matrix.server_name",
        default="dms.vertel.se",
    )
    mail_matrix_matrix_domain = fields.Char(
        string="Matrix Domain",
        config_parameter="mail_matrix.matrix_domain",
    )
    mail_matrix_server_url = fields.Char(
        string="Homeserver URL",
        config_parameter="mail_matrix.server_url",
    )
    mail_matrix_bot_token = fields.Char(
        string="Appservice Token",
        config_parameter="mail_matrix.bot_token",
    )
    mail_matrix_hs_token = fields.Char(
        string="Homeserver Token",
        config_parameter="mail_matrix.hs_token",
    )
    mail_matrix_webhook_token = fields.Char(
        string="Legacy Webhook Token",
        config_parameter="mail_matrix.webhook_token",
    )
    mail_matrix_appservice_endpoint = fields.Char(
        string="Appservice Endpoint",
        config_parameter="mail_matrix.appservice_endpoint",
        default="/mail/matrix/appservice",
    )
