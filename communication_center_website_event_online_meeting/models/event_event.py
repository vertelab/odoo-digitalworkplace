from odoo import models, fields, api, _
from odoo.exceptions import UserError

import uuid
import string, random


class Event(models.Model):
    _inherit = 'event.event'

    online_meeting_link = fields.Char(string="Meeting Link")
    video_meeting_checkbox = fields.Boolean(string="Video Meeting")


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    select_roles = fields.Selection([('Moderator', 'moderator'), ('Audience', 'audience'), ('Presenter', 'presenter')],
                                    string="Select Roles")
