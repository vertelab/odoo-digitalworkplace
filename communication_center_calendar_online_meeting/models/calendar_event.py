from odoo import models, fields, api, _


class Meeting(models.Model):
    _inherit = 'calendar.event'

    online_meeting_link = fields.Char(string="Meeting Link")

    def create_meeting_link(self):
        pass
