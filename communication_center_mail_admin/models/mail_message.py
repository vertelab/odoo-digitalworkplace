# -*- coding: utf-8 -*-
################################################################################
#   See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import fields, models, _
from odoo.exceptions import ValidationError
from odoo import tools


class Message(models.Model):
    _inherit = "mail.message"

    history_line = fields.One2many(
        'mail.message.history', 'mail_message_id',
        string='History Line', copy=True, auto_join=True
    )

    def unlink(self):
        wk_has_delete = self.env['ir.config_parameter'].sudo().get_param('communication_center_mail_admin.has_delete', False)
        if self._context.get('wkDeleteFlag') and not wk_has_delete:
            raise ValidationError(_("The requested operation cannot be completed due to security restrictions. Please contact your system administrator."))
        return super(Message, self).unlink()

    def checkWkEdit(self):
        wk_has_edit = self.env['ir.config_parameter'].sudo().get_param('communication_center_mail_admin.has_edit', False)
        if not wk_has_edit:
            raise ValidationError(_("The requested operation cannot be completed due to security restrictions. Please contact your system administrator."))
        return True

    def message_format(self):
        message_values = super(Message, self).message_format()
        edit = self.env['ir.config_parameter'].sudo().get_param('communication_center_mail_admin.has_edit') == "True" or False
        delete = self.env['ir.config_parameter'].sudo().get_param('communication_center_mail_admin.has_delete') == "True" or False
        mail_message = self.env['mail.message']
        for message in message_values:
            message['wk_edit'] = edit
            message['wk_delete'] = delete
            message['wk_is_updated'] = False
            wk_last_updated_on = mail_message.search([('id', '=', message['id'])])
            if wk_last_updated_on.history_line:
                history_line = wk_last_updated_on.history_line[0]
                message['wk_is_updated'] = True
                message['wk_last_updated_on'] = history_line.create_date
        return message_values

    def write(self, vals):
        wk_has_edit = self.env['ir.config_parameter'].sudo().get_param('communication_center_mail_admin.has_edit', False)
        if wk_has_edit and self.env.user.user_has_groups('communication_center_mail_admin.group_wk_history') and 'body' in vals:
            old_body = tools.html2plaintext(self.body)
            new_body = tools.html2plaintext(vals['body'])
            if old_body != new_body:
                self.env['mail.message.history'].create({
                    'mail_message_id': self.id,
                    'old_body': old_body,
                    'new_body': new_body
                })
        return super(Message, self).write(vals)

    def edit_message_format(self):
        messages = self.read()
        mail_message = self.env['mail.message']
        for message in messages:
            message['wk_is_updated'] = False
            wk_last_updated_on = mail_message.search([('id', '=', message['id'])])
            if wk_last_updated_on.history_line:
                history_line = wk_last_updated_on.history_line[0]
                message['wk_is_updated'] = True
                message['wk_last_updated_on'] = history_line.create_date
        return messages
