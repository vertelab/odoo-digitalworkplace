# -*- coding: utf-8 -*-
#################################################################################
#
#   See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    wk_has_edit = fields.Boolean(
        string='Edit',
        config_parameter='communication_center_mail_admin.has_edit',
        help="Edit option for Send message & Log note."
    )
    wk_has_delete = fields.Boolean(
        string='Delete',
        config_parameter='communication_center_mail_admin.has_delete',
        help="Delete option for Send message & Log note."
    )
    group_wk_history = fields.Boolean(
        string='Manage History',
        implied_group='communication_center_mail_admin.group_wk_history',
        help="History tracking for Send message & Log note."
    )
