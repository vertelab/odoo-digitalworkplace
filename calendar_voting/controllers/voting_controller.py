from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class VotingController(http.Controller):

    @http.route(['/voting_calendar/<int:event_id>'], type="http", auth='public', website=True)
    def voting_site(self, event_id, **kw):
        event = request.env["calendar.event"].browse(event_id)
        my_voting = request.env["calendar.voting"].sudo().search([("event_id", "=", event_id),("partner_id", "=", request.env.user.partner_id.id)])
        votings = request.env["calendar.voting"].sudo().search([("event_id", "=", event_id)])- my_voting
        return request.render("calendar_voting.calendar_voting_site", {"event":event, "votings":votings, "my_voting":my_voting})


    @http.route(['/voting_calendar/<int:event_id>/<string:token>'], type="http", auth='public', website=True)
    def voting_site_token(self, event_id, token, **kw):
        if token:
            event = request.env["calendar.event"].sudo().browse(event_id)
            my_voting = request.env["calendar.voting"].sudo().search([("event_id", "=", event_id),("access_token", "=", token)])
            if my_voting:
                votings = request.env["calendar.voting"].sudo().search([("event_id", "=", event_id)])
                votings = votings - my_voting
                return request.render("calendar_voting.calendar_voting_site", {"event":event, "votings":votings, "my_voting":my_voting})
        return request.render("website.page_404")
