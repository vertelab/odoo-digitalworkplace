from venv import create
from odoo import models, fields, api, _
from odoo.exceptions import UserError

import uuid
import string, random, logging

_logger = logging.getLogger(__name__)
class Meeting(models.Model):
    _inherit = 'calendar.event'

    url_link = fields.Char(string="Url")
    microphone_off = fields.Boolean(string="Microphone off")
    webcam_off = fields.Boolean(string="Webcam off")
    lobby_with_name = fields.Boolean(string="Start a lobby, participants enterin ther name is required")
    #lobby_with_drop_in?
    link_for_participants = fields.Boolean(string="Link for participants")
    link_for_moderator = fields.Boolean(string="Link for moderator")
    no_recording = fields.Boolean(string="Turn off the possibility to record")
    start_recording = fields.Boolean(string="Start recording from beginning off the meeting")
    rooms_creation = fields.Boolean(string="Create and move participants to roomes")
    #one select?
    help_for_button = fields.Text()


    def create_meeting_link(self):
        jitsi_url = self.env['ir.config_parameter'].get_param('jitsi_url')
        if not jitsi_url:
            raise UserError(_("Kindly set a Jitsi URL"))
        link_suffix = ''.join(random.choices(string.ascii_letters, k=8))
        if self.online_meeting_link is False:
            #link_suffix = ''.join(random.choices(string.ascii_letters, k=8))
            self.online_meeting_link = f"{jitsi_url}/{link_suffix}#"
       # elif self.online_meeting_link is True:
        _logger.error(f"{jitsi_url}/{link_suffix}#")

    @api.model
    def get_values(self):
        link = super(Meeting, self).get_link()
        icp = self.env['ir.config_parameter'].sudo()
        link.update({
            'jitsi_url': icp.get_param('online_meeting_link')
        })
        return link

    @api.onchange("video_meeting_chekbox", "microphone_off", "webcam_off")
    def video_settings(self):
        #jitsi_url = self.env['ir.config_parameter'].get_param('jitsi_url')
        self.create_meeting_link()
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
