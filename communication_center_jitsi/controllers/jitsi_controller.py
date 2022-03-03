from asyncio.log import logger
from odoo.http import request
from odoo import http, api, models, fields, _

import logging, string, random

_logger = logging.getLogger(__name__)

class JitsiController(http.Controller):
    _inherit ="jitsi.controller"


    @http.route(['/video_meeting/<string:link_suffix>'], type="http", auth='public', website=True)
    def meeting(self, link_suffix, **kw):
        event = self.get_event(link_suffix)
        jitsi = self.create_jitsi_link(link_suffix)
        return request.render("communication_center_jitsi.jitsi_meeting_site", {"event": event, "jitsi": jitsi})

    def get_event(self, link_suffix):
        event = request.env["calendar.event"].sudo().search([('link_suffix', '=', link_suffix)])
        _logger.warning(f'event, {event}')
        return event

    def create_jitsi_link(self, link_suffix):
        event = request.env["calendar.event"].sudo().search([('link_suffix', '=', link_suffix)])
        jitsi_url = event.env['ir.config_parameter'].get_param('jitsi_url')
        _logger.error(f'jitsi_url, {jitsi_url}')
        jitsi = f'{jitsi_url}/{link_suffix}'
        _logger.error(f'jitsi, {jitsi}')
        return jitsi

    def get_roomName (self, room_name):
        room = request.env["calendar.event"].sudo().search([('room_name', '=', room_name)])
        return room

    @api.model
    def json_get (self, options):
        getoptions = request.env["meeting_settings.js"].sudo().search([('options', '=', options)])
        return options

#not working at the moment, neds to stay becuas its needed for future coding

    # @api.onchange("video_meeting_checkbox", "microphone_off", "webcam_off")
    # def video_settings(self):
    #     event = self.env["calendar.event"].browse(id)
    #     event.get_event()
    #     if self.microphone_off is True:
    #         self.online_meeting_link += "config.startWithAudioMuted=true&"
    #     elif self.microphone_off is False:
    #         x = self.online_meeting_link.replace("config.startWithAudioMuted=true&","")
    #         self.online_meeting_link = x
            
    #     if self.webcam_off is True:
    #         self.online_meeting_link += "config.startWithVideoMuted=true&"
    #     elif self.webcam_off is False:
    #         x = self.online_meeting_link.replace("config.startWithVideoMuted=true&","")
    #         self.online_meeting_link = x
