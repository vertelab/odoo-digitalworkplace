# -*- coding: utf-8 -*-

from . import models
from . import wizard
from odoo.service import common
# odoo.exceptions.Warning was removed in 16.0; UserError replaced it.
from odoo.exceptions import UserError as Warning


def pre_init_check(cr):
    version_info = common.exp_version()
    server_series = version_info.get('server_serie')
    if server_series != '14.0':
        raise Warning('Module support Odoo series 14.0 found {}'.format(server_series))
    return True
