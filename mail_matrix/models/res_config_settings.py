# -*- coding: utf-8 -*-
# Copyright (C) 2026 Vertel AB (<https://vertel.se>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # These fields back the ir.config_parameter keys that the module already
    # reads at runtime (see controllers/main.py and publisher/matrix_publisher.py).
    # They are declared here because res.config.settings fields must exist in
    # Python before a view can reference them — a view pointing at undefined
    # fields aborts the whole registry.
    mail_matrix_matrix_domain = fields.Char(
        string='Matrix Domain',
        config_parameter='mail_matrix.matrix_domain',
    )
    mail_matrix_webhook_token = fields.Char(
        string='Webhook Token',
        config_parameter='mail_matrix.webhook_token',
    )
    mail_matrix_rabbitmq_host = fields.Char(
        string='RabbitMQ Host',
        config_parameter='mail_matrix.rabbitmq_host',
    )
    mail_matrix_rabbitmq_port = fields.Char(
        string='RabbitMQ Port',
        config_parameter='mail_matrix.rabbitmq_port',
    )
    mail_matrix_rabbitmq_vhost = fields.Char(
        string='RabbitMQ Vhost',
        config_parameter='mail_matrix.rabbitmq_vhost',
    )
    mail_matrix_rabbitmq_user = fields.Char(
        string='RabbitMQ User',
        config_parameter='mail_matrix.rabbitmq_user',
    )
    mail_matrix_rabbitmq_password = fields.Char(
        string='RabbitMQ Password',
        config_parameter='mail_matrix.rabbitmq_password',
    )
    mail_matrix_rabbitmq_exchange = fields.Char(
        string='RabbitMQ Exchange',
        config_parameter='mail_matrix.rabbitmq_exchange',
    )
