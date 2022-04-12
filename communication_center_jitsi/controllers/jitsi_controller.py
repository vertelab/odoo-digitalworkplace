from asyncio.log import logger
from odoo.http import request
from odoo import http, api, models, fields, _

import logging, string, random

_logger = logging.getLogger(__name__)

class JitsiController(http.Controller):
    _inherit ="jitsi.controller"


    @http.route(['/video_meeting/<string:link_suffix>'], type="http", auth='public', website=True)
    def meeting(self, link_suffix, **kw):
        event = self._get_event(link_suffix)
        jitsi = self._create_jitsi_link(link_suffix)
        return request.render("communication_center_jitsi.jitsi_meeting_site", {"event": event, "jitsi": jitsi})

    def _get_event(self, link_suffix):
        event = request.env["calendar.event"].sudo().search([('link_suffix', '=', link_suffix)])
        _logger.warning(f'event, {event}')
        fields = event.fields_get()
        for key in sorted(fields.keys()):
            _logger.error(f'event.{key}:{event[key]}')
        return event

    def _create_jitsi_link(self, link_suffix):
        event = request.env["calendar.event"].sudo().search([('link_suffix', '=', link_suffix)])
        jitsi_url = event.env['ir.config_parameter'].get_param('jitsi_url')
        link = f'{jitsi_url}'
        _logger.error(f'jitsi_url, {jitsi_url}')
        _logger.error(f'jitsi, {link}')
        return link

#/{link_suffix}