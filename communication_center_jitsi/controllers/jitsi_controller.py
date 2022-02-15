
from odoo.http import request
from odoo import http

class TestingStuff(http.Controller):

    @http.route(['/hello/'], type="http", auth='public', website=True)
    def testing(self, **kw):
        #return "Testing"
        return request.render("communication_center_jitsi.test_padge", {})

    #@http.route(['/video-test-meeting/'], type="http", auth='public', website=True)
    #def testing_meeting(self, **kwargs):
    #    return request.render("")