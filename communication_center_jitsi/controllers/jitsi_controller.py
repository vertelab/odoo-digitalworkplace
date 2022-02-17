from odoo.http import request
from odoo import http

class JitsiController(http.Controller):
    _inherit ="jitsi.controller"

    @http.route(['/video_meeting/'], type="http", auth='public', website=True)
    def testing(self, **kw):
        #return "Testing"
        return request.render("communication_center_jitsi.jitsi_meeting_site", {})

    #se till att controllern kan axeptera unika id;n

    #def controller_meeting_link(self):
     #   jitsi_url = self.env['ir.config_parameter'].get_param('jitsi_url')
      #  self.online_meeting_link = f"{jitsi_url}/{self.create_meeting_link_part()}#"