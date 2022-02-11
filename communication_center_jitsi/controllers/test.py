
from odoo.http import request
from odoo import http

class TestingStuff(http.Controller):

    @http.route(['/hello/'], type="http", auth='public', website=True)
    def testing(self, **kw):
        #return "Testing"
        return request.render("communication_center_jitsi.meeting_settings", {})