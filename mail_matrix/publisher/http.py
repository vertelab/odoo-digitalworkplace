# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2025- Vertel AB (<https://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
##############################################################################

"""Low-level HTTP helper for Matrix client-server API calls."""

import json
import logging

import requests

_logger = logging.getLogger(__name__)

TIMEOUT = 15


def matrix_request(homeserver_url, method, path, body=None, token=None):
    """Perform a Matrix client-server API request.

    Args:
        homeserver_url: base URL e.g. https://matrix.dms.vertel.se
        method: HTTP method (GET/POST/PUT)
        path: API path e.g. /_matrix/client/v3/createRoom
        body: JSON payload (dict)
        token: access token (appservice or user)
    Returns:
        JSON response dict, or {"error": ...} on failure.
    """
    url = homeserver_url.rstrip("/") + path
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer %s" % token
    try:
        resp = requests.request(
            method, url, json=body, headers=headers, timeout=TIMEOUT
        )
        if resp.status_code >= 200 and resp.status_code < 300:
            return resp.json() if resp.content else {}
        try:
            data = resp.json()
        except Exception:
            data = {"raw": resp.text[:200]}
        return {"error": data, "code": resp.status_code}
    except requests.RequestException as e:
        _logger.error("Matrix request %s %s failed: %s", method, url, e)
        return {"error": str(e), "code": 0}