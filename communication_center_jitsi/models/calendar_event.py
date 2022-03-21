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
    controller_link = fields.Char(string="Video meeting link", default = " ")
    link_suffix = fields.Char(string='Unique ID of Event')

    @api.onchange("controller_link","video_meeting_checkbox")
    def link_to_controller(self):
        if not self.link_suffix:
            self.link_suffix = ''.join(random.choices(string.ascii_letters, k=8))
        if not self.video_meeting_checkbox:
            # web_name = self.env['ir.config_parameter'].get_param('web.base.url')
            # _logger.error(f'web_name, {web_name}')
            # if self.video_meeting_checkbox == 0:
            #     clean_link = f'{web_name}/video_meeting/{self.link_suffix}'
            #     _logger.error(f'clean_link, {clean_link}')
            self.controller_link = self.create_controller_link(self.link_suffix )
                # _logger.error(f'self.link_suffix, {self.link_suffix}')
                # _logger.error(f'self.controller_link {self.controller_link}')


    def create_controller_link(self, link_suffix):
        web_name = self.env['ir.config_parameter'].get_param('web.base.url')
        _logger.error(f"create_controller_link {link_suffix=}")
        return f'{web_name}/video_meeting/{link_suffix}'


    @api.model
    def create(self, vals):
        _logger.error(f"{vals=}")
        if  vals.get("video_meeting_checkbox"):
            vals["controller_link"] = self.create_controller_link(vals.get("link_suffix"))
            _logger.error(f"true {vals=}")
        res = super().create(vals)
        _logger.error(f"{res=}")
        return res

    def write(self, vals):
        _logger.error(f"{vals=}")
        for rec in self:
            if vals.get("video_meeting_checkbox"):
                vals["controller_link"] = rec.create_controller_link(rec.link_suffix or vals.get("link_suffix"))
                _logger.error(f"write {vals=}")
            elif "video_meeting_checkbox" in vals:
                vals["controller_link"] = " "

            res = super().write(vals)
            # if not rec.video_meeting_checkbox:
            _logger.error(f"{res=}")
            return res
