from asyncio.log import logger
from odoo.http import request
from odoo import http, api, models, fields, _

import logging, string, random
#from communication_center_jitsi.models import calendar_event

_logger = logging.getLogger(__name__)

class JitsiController(http.Controller):
    _inherit ="jitsi.controller"



    @http.route(['/video_meeting/<string:link_suffix>'], type="http", auth='public', website=True)
    def meeting(self, link_suffix, **kw):
        event = self.create_meeting_link(link_suffix)
        jitsi = self.create_jitsi_link(link_suffix)
        #set_room = self.get_roomName(room_name)
        return request.render("communication_center_jitsi.jitsi_meeting_site", {"event": event, "jitsi": jitsi}) #läg in jitsi som eventet, gör att du kan få tag på den i xml som event

    def create_meeting_link(self, link_suffix):
        # Find matching event that has the correct UID ending.
        event = request.env["calendar.event"].sudo().search([('link_suffix', '=', link_suffix)])
        #event = request.env["calendar.event"].browse(event_id)
        if event:
            if event.link_suffix == link_suffix:
                _logger.error(f"hawow?{event}")
                return event

    def create_jitsi_link(self, link_suffix): #gör inget just nu
        #event = request.env["calendar.event"].browse(event_id)
        event = request.env["calendar.event"].sudo().search([('link_suffix', '=', link_suffix)])
        jitsi_url = event.env['ir.config_parameter'].get_param('jitsi_url')
        _logger.error(f'hello?{jitsi_url}')
        if event:
            if event.link_suffix == link_suffix:
                jitsi = f'{jitsi_url}/{link_suffix}'
                _logger.error(f'MAdyw{jitsi}')
                return jitsi
    #_logger.error(f'LÄNK{event}') #kalelse på calendar.event()
    #_logger.error(f'hello?{jitsi_url}') #jitsi_url;n
        # sätt /roomName
        #/link_suffix

    def get_roomName (self, room_name):
        room = request.env["calendar.event"].sudo().search([('room_name', '=', room_name)])
        #event = request.env["calendar.event"].sudo().search([('link_suffix', '=', link_suffix)])
        #jitsi_url = event.env['ir.config_parameter'].get_param('jitsi_url')
        if room:
            if room.room_name == room_name:
                set_room = f'{room_name}'
                return set_room


    @api.model
    def json_get (self, options):
        getoptions = request.env["meeting_settings.js"].sudo().search([('options', '=', options)])
        if getoptions:
            if getoptions.options == options:
                return options


    #få kamran och micen att funka först, få sedan detta att funka
    #byt eller skapa online_meeting_link, just nu används den inte/är inget [22feb]
    @api.onchange("video_meeting_chekbox", "microphone_off", "webcam_off")
    def video_settings(self):
        event = self.env["calendar.event"].browse(id)
        event.create_meeting_link()
        if self.microphone_off is True:
            self.online_meeting_link += "config.startWithAudioMuted=true&"
        elif self.microphone_off is False:
            x = self.online_meeting_link.replace("config.startWithAudioMuted=true&","")
            self.online_meeting_link = x
            
        if self.webcam_off is True:
            self.online_meeting_link += "config.startWithVideoMuted=true&"
        elif self.webcam_off is False:
            x = self.online_meeting_link.replace("config.startWithVideoMuted=true&","")
            self.online_meeting_link = x


    #<int:id>/'