from odoo import models, fields, api, _


class Meeting(models.Model):
    _inherit = 'calendar.event'

    online_meeting_link = fields.Char( string="Meeting Link")
    video_meeting_chekbox = fields.Boolean(string ="Video Meeting")
    #url_link = fields.Char(string="Url")

   # @api.onchange("video_meeting_chekbox")
    #def hide_link(self):
     #   if self.video_meeting_chekbox != False:
      #      self.online_meeting_link != 'invisible'

    def create_meeting_link(self):
        pass

#readonly=True