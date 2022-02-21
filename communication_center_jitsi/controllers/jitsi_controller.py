from asyncio.log import logger
from odoo.http import request
from odoo import http, api, models, fields, _

import logging, string, random
#from communication_center_jitsi.models import calendar_event

_logger = logging.getLogger(__name__)

class JitsiController(http.Controller):
    _inherit ="jitsi.controller"



    @http.route(['/video_meeting/<string:link_suffix>/'], type="http", auth='public', website=True)
    def meeting(self, link_suffix, **kw):
        link = self.create_meeting_link(link_suffix)
        _logger.error(f"{kw}")
        return request.render("communication_center_jitsi.jitsi_meeting_site", {})
    _logger.error("YOU WORK!?")

    def create_meeting_link(self, link_suffix):
        # Find matching event that has the correct UID ending.
        event = request.env["calendar.event"].search([('link_suffix', '=', link_suffix)])
        jitsi_url = event.env['ir.config_parameter'].get_param('jitsi_url')
        #link_suffix = ''.join(random.choices(string.ascii_letters, k=8))
        _logger.error(f'hello?{jitsi_url}')
        if not event.online_meeting_link:
            pass
            
    @api.onchange("video_meeting_chekbox", "microphone_off", "webcam_off")
    def video_settings(self):
        event = self.env["calendar.event"].browse(id)
        event.create_meeting_link()
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


    #<int:id>/'