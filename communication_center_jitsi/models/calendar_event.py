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
    lobby_with_name = fields.Boolean( string="Start a lobby, name is required")
    lobby_with_let_in = fields.Boolean(string="Start a lobby, with name and knocking to get in")
    link_for_participants = fields.Boolean(string="Link for participants")
    link_for_moderator = fields.Boolean(string="Link for moderator")
    no_recording = fields.Boolean(string="Turn off the possibility to record")
    start_recording = fields.Boolean(string="Start recording from beginning off the meeting")
    rooms_creation = fields.Boolean(string="Create and move participants to roomes")
    room_name = fields.Char(string="Enter room name")
    controller_link = fields.Char(string="Video meeting link", default = " ")
    link_suffix = fields.Char(string='Unique ID of Event')

    @api.onchange("controller_link","video_meeting_checkbox")
    def link_to_controller(self):
        if not self.link_suffix:
            self.link_suffix = ''.join(random.choices(string.ascii_letters, k=10)).lower()
            self.link_suffix
        if not self.video_meeting_checkbox:
            self.controller_link = self.create_controller_link(self.link_suffix)


    def create_controller_link(self, link_suffix):
        web_name = self.env['ir.config_parameter'].get_param('web.base.url')
        return f'{web_name}/video_meeting/{link_suffix}'


    @api.model
    def create(self, vals):
        if  vals.get("video_meeting_checkbox"):
            vals["controller_link"] = self.create_controller_link(vals.get("link_suffix"))
        res = super().create(vals)
        return res

    def write(self, vals):
        for rec in self:
            if vals.get("video_meeting_checkbox"):
                vals["controller_link"] = rec.create_controller_link(rec.link_suffix or vals.get("link_suffix"))
                _logger.error(f"write {vals=}")
            elif "video_meeting_checkbox" in vals:
                vals["controller_link"] = " "

            res = super().write(vals)
            return res
