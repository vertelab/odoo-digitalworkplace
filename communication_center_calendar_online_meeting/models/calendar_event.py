from odoo import models, fields, api, _


class Meeting(models.Model):
    _inherit = 'calendar.event'

    online_meeting_link = fields.Char( string="Meeting Link")
    video_meeting_chekbox = fields.Boolean(string ="Video Meeting")
    #url_link = fields.Char(string="Url")

    def create_meeting_link(self):
        pass

#readonly=True