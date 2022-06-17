from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class VotingController(http.Controller):

    @http.route(['/voting_calendar/<int:event_id>'], type="http", auth='public', website=True)
    def voting_site(self, event_id, **kw):
        event = request.env["calendar.event"].browse(event_id)
        votings = request.env["calendar.voting"].sudo().search([("event_id", "=", str(event_id))])
        _logger.error(f"{votings=}")
        return request.render("calendar_voting.calendar_voting_site", {"event":event, "votings":votings})
        
#TODO: Add tokens to know witch user is voting: 
# https://github.com/vertelab/odoo-sale/blob/14.0/sale_multi_approval/controllers/main.py 
# approval_id and _document_check_access
