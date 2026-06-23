"""RabbitMQ publisher for Matrix messages.

Publishes Odoo chat messages to the odoo.messages topic exchange
for consumption by the matrix-consumer systemd service.
"""

import json
import logging

_logger = logging.getLogger(__name__)

# Default connection params — overridable via system parameters
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 5672
DEFAULT_VHOST = "/"
DEFAULT_USER = "matrix"
DEFAULT_PASSWORD = "matrix"
DEFAULT_EXCHANGE = "odoo.messages"


def _get_connection_params(env):
    """Read RabbitMQ connection params from ir.config_parameter."""
    get_param = env["ir.config_parameter"].sudo().get_param
    return {
        "host": get_param("mail_matrix.rabbitmq_host", DEFAULT_HOST),
        "port": int(get_param("mail_matrix.rabbitmq_port", DEFAULT_PORT)),
        "vhost": get_param("mail_matrix.rabbitmq_vhost", DEFAULT_VHOST),
        "user": get_param("mail_matrix.rabbitmq_user", DEFAULT_USER),
        "password": get_param("mail_matrix.rabbitmq_password", DEFAULT_PASSWORD),
        "exchange": get_param("mail_matrix.rabbitmq_exchange", DEFAULT_EXCHANGE),
    }


def publish_message(payload):
    """Publish a message to RabbitMQ for Matrix routing.
    
    Args:
        payload: dict with message data including matrix_recipients.
    """
    import pika

    # Get connection params from Odoo env (if available)
    try:
        from odoo import api
        env = api.Environment.manage()
        # We run outside Odoo context in simple cases
        params = _get_connection_params(env) if env else {}
    except Exception:
        params = {}

    host = params.get("host", DEFAULT_HOST)
    port = params.get("port", DEFAULT_PORT)
    vhost = params.get("vhost", DEFAULT_VHOST)
    user = params.get("user", DEFAULT_USER)
    password = params.get("password", DEFAULT_PASSWORD)
    exchange = params.get("exchange", DEFAULT_EXCHANGE)

    credentials = pika.PlainCredentials(user, password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=vhost,
            credentials=credentials,
            heartbeat=600,
        )
    )
    channel = connection.channel()

    # Publish to each recipient with matrix.<matrix_id> routing key
    message_body = json.dumps(payload, default=str)
    for recipient_id in payload.get("matrix_recipients", []):
        routing_key = f"matrix.{recipient_id}"
        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message_body.encode("utf-8"),
            properties=pika.BasicProperties(
                delivery_mode=2,  # persistent
                content_type="application/json",
            ),
        )
        _logger.debug(
            "Published to %s with routing key %s", exchange, routing_key
        )

    connection.close()
    return True
