from odoo import models, fields, api, _
from odoo.exceptions import UserError

import uuid
import string, random


class Meeting(models.Model):
    _inherit = 'calendar.event'

    def create_meeting_link(self):
        jitsi_url = self.env['ir.config_parameter'].get_param('jitsi_url')
        if not jitsi_url:
            raise UserError(_("Kindly set a Jitsi URL"))
        link_suffix = ''.join(random.choices(string.ascii_letters, k=8))
        self.online_meeting_link = f"{jitsi_url}/{link_suffix}"
        return super(Meeting, self).create_meeting_link()
