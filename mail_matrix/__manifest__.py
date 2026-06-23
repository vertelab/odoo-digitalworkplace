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
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Workplace: Mail Matrix Bridge",
    "version": "0.0.1",
    "summary": "Bridge Odoo mail/chat with Matrix protocol via RabbitMQ.",
    "category": "Productivity",
    "description": """
Bridge Odoo mail/chat with Matrix protocol via RabbitMQ.

Outbound: Odoo chat message -> Publisher -> RabbitMQ -> Consumer -> Matrix API
Inbound: Matrix message -> Webhook -> Odoo controller -> mail.message

- Adds matrix_id field to res.partner
- Publishes chat messages to RabbitMQ odoo.messages exchange
- Webhook endpoint for Matrix -> Odoo inbound messages
- .well-known/matrix/server delegation endpoint
    """,
    "sequence": "290",
    "author": "Vertel AB",
    "website": "https://vertel.se/apps/odoo-digitalworkplace/mail_matrix",
    "license": "AGPL-3",
    "contributor": "",
    "maintainer": "Vertel AB",
    "repository": "https://github.com/vertelab/odoo-digitalworkplace",
    "depends": ["mail", "base"],
    "data": [
        "views/res_partner_view.xml",
        "views/res_config_settings.xml",
        "security/ir.model.access.csv",
    ],
    "application": True,
}
