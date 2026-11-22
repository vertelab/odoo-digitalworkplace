from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class DiscoveryController(http.Controller):

    @http.route(['/well-known/carddav/'], type="http", auth='public', website=True)
    def handle_discovery_request(self, **kw):
        if kw:
            _logger.warning(kw);
#        return request.render("website.page_404")
        return 'Hello world'
