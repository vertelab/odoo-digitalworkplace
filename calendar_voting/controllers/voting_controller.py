from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class VotingController(http.Controller):

    @http.route(['/voting_calendar/<int:event_id>'], type="http", auth='public', website=True)
    def voting_site(self, event_id, **kw):
        event = request.env["calendar.event"].browse(event_id)
        return request.render("calendar_voting.calendar_voting_site", {"event":event})
        
#TODO: Send JWT tokends with the mail invite 
# ,when voting is over the participants can not vote anymore but can still se the the resalts
