# -*- coding: utf-8 -*-
#################################################################################
#
#   See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import fields, models


class MailMessageHistory(models.Model):
    _name = 'mail.message.history'
    _description = 'Mail Message History'
    _order = 'id desc'

    mail_message_id = fields.Many2one(
        'mail.message', string='Message Reference',
        required=True, ondelete='cascade',
        index=True, copy=False
    )
    old_body = fields.Char(string='Old Body', readonly=True)
    new_body = fields.Char(string='New Body', readonly=True)
