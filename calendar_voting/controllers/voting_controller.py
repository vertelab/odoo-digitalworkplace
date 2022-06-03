from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class VotingController(http.Controller):

    @http.route(['/voting_calendar'], type="http", auth='public', website=True)
    def voting_site(self, **kw):
        return request.render("calendar_voting.calendar_voting_site")
        