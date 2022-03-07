from distutils.command.clean import clean
import json
import logging
import random
import string

from odoo import models, fields, api, _, http
from odoo.http import request
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class Meeting(models.Model):
    _inherit = 'calendar.event'

    url_link = fields.Char(string="Url")
    microphone_off = fields.Boolean(string="Microphone off")
    webcam_off = fields.Boolean(string="Webcam off")
    lobby_with_name = fields.Boolean( string="Start a lobby, participants enterin ther name is required")
    lobby_with_let_in = fields.Boolean(string="Lobby, chuse how get let in")
    link_for_participants = fields.Boolean(string="Link for participants")
    link_for_moderator = fields.Boolean(string="Link for moderator")
    no_recording = fields.Boolean(string="Turn off the possibility to record")
    start_recording = fields.Boolean(string="Start recording from beginning off the meeting")
    rooms_creation = fields.Boolean(string="Create and move participants to roomes")
    help_for_button = fields.Text()
    room_name = fields.Char(string="Enter room name")
#REMEMBER: dont set controller_link to readonly, it gives error
    controller_link = fields.Char(string="Video meeting link")
    link_suffix = fields.Char(string='Unique ID of Event')

    @api.onchange("controller_link")
    def link_to_controller(self):
        if not self.link_suffix:
            self.link_suffix = ''.join(random.choices(string.ascii_letters, k=8))
        if self.video_meeting_checkbox == 0:
            web_name = self.env['ir.config_parameter'].get_param('web.base.url')
            _logger.error(f'web_name, {web_name}')
            if self.video_meeting_checkbox == 0:
                clean_link = f'{web_name}/video_meeting/{self.link_suffix}'
                _logger.error(f'clean_link, {clean_link}')
                self.controller_link = clean_link
                _logger.error(f'self.link_suffix, {self.link_suffix}')
                _logger.error(f'self.controller_link {self.controller_link}')



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