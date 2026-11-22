# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2025- Vertel Sverige AB (<https://vertel.se>).
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
    "version": "0.0.6",
    "summary": "Bridge Odoo mail/chat with Matrix protocol via RabbitMQ.",
    "category": "Productivity",
    "description": """
Bridge Odoo mail/chat with Matrix via the Matrix appservice protocol.

Inbound: Matrix message -> /mail/matrix/appservice -> mail.message
Outbound: Odoo chat message -> Matrix client API (appservice token)

- Adds matrix_id field to res.partner
- Adds matrix_localpart to res.users (incl. AI coworkers)
- matrix.room.binding maps Matrix rooms to discuss.channel
- Appservice endpoint /mail/matrix/appservice (hs_token auth)
- .well-known/matrix/server delegation endpoint
    """,
    "sequence": "290",
    "author": "Vertel Sverige AB",
    "website": "https://vertel.se/apps/odoo-digitalworkplace/mail_matrix",
    "license": "AGPL-3",
    "contributor": "",
    "maintainer": "Vertel Sverige AB",
    "repository": "https://github.com/vertelab/odoo-digitalworkplace",
    "depends": ["mail", "base"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_view.xml",
        "views/res_config_settings.xml",
    ],
    "application": True,
}
