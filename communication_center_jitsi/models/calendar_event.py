import json
import logging
import random
import string

from odoo import models, fields, api, _
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
        if self.video_meeting_chekbox == 0:
            x = "http://alex-14:8069/video_meeting/"+f"{self.link_suffix}"
            self.controller_link = x.replace("NewId_","")
            _logger.error(f'self.link_suffix, {self.link_suffix}')
            _logger.error(f'self.controller_link {self.controller_link}')
