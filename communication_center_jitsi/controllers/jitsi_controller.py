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
       # _logger.warning(f'event, {event}')
        #_logger.warning(f'event, {dir(event)}')
       # _logger.warning(f'event, {event.fields_get()}')
        fields = event.fields_get()
       # for key in sorted(fields.keys()):
       #     _logger.error(f'event.{key}:{event[key]}')
        return event

    def _create_jitsi_link(self, link_suffix):
        event = request.env["calendar.event"].sudo().search([('link_suffix', '=', link_suffix)])
        jitsi_url = event.env['ir.config_parameter'].get_param('jitsi_url')
       # _logger.error(f'jitsi_url, {jitsi_url}')
        link = f'{jitsi_url}/{link_suffix}'
       # _logger.error(f'jitsi, {link}')
        return link

    # def _get_roomName (self, room_name):
    #     room = request.env["calendar.event"].sudo().search([('room_name', '=', room_name)])
    #     return room

    # @api.model
    # def _json_get (self, options):
    #     getoptions = request.env["meeting_settings.js"].sudo().search([('options', '=', options)])
    #     return options

#not working at the moment, neds to stay becuas its needed for future coding
#controler_link from calenadr.event 

    # @api.onchange("microphone_off")
    # def  _video_settings (self, microphone_off):
    #     request.env["calendar.event"].sudo().search([('microphone_off', '=', microphone_off)])
    #     real_url = "#"
    #     if microphone_off is True:
    #         real_url += "config.startWithAudioMuted=true&"
    #     elif microphone_off is False:
    #         real_url.replace("config.startWithAudioMuted=true&","")
    #     return real_url

    # @api.onchange ("microphone_off")
    # def _video_settings (self, link_suffix, microphone_off):
    #     request.env["calendar.event"].sudo().search([('link_suffix', '=', link_suffix)])
    #     real_url = self._create_jitsi_link(link_suffix)
    #     request.env["calendar.event"].sudo().search([('microphone_off', '=', microphone_off)])
    #     if microphone_off is True:
    #         real_url += "config.startWithAudioMuted=true&"
    #     elif microphone_off is False:
    #         url_plus = real_url.replace("config.startWithAudioMuted=true&","")
    #         real_url = url_plus

        
    # @api.onchange("video_meeting_checkbox", "microphone_off", "webcam_off")
    # def video_settings(self, microphone_off):
    #     request.env["calendar.event"].sudo().search([('microphone_off', '=', microphone_off)])
    #     #event = self.env["calendar.event"].browse(id)
    #     # event._get_event()
    #     url_plus = self._create_jitsi_link()
    #     _logger.error(f'link1, {url_plus}')
    #     if microphone_off is True:
    #         url_plus += "config.startWithAudioMuted=true&"
    #         _logger.error(f'link2, {url_plus}')
    #     elif microphone_off is False:
    #         x = url_plus.replace("config.startWithAudioMuted=true&","")
    #         url_plus = x
    #         _logger.error(f'link3, {url_plus}')
            
    #     if self.webcam_off is True:
    #         self.online_meeting_link += "config.startWithVideoMuted=true&"
    #     elif self.webcam_off is False:
    #         x = self.online_meeting_link.replace("config.startWithVideoMuted=true&","")
    #         self.online_meeting_link = x
