from odoo import api, fields, models


class EditHistory(models.TransientModel):
    _name = 'edit.history'
    _description = 'Edit History'
    _order = 'id desc'
    _rec_name = 'edit_message_log_note_id'

    edit_message_log_note_id = fields.Many2one(
        'edit.message.log.note',
        required=True, ondelete='cascade',
        index=True, copy=False
    )
    old_body = fields.Char(string='Old Body', readonly=True)
    new_body = fields.Char(string='New Body', readonly=True)
    create_date = fields.Datetime(readonly=True)


class EditMessageLogNote(models.TransientModel):
    _name = 'edit.message.log.note'
    _description = 'Edit Message Log Note'
    _rec_name = 'mail_message_id'

    @api.model
    def default_get(self, fields):
        result = super(EditMessageLogNote, self).default_get(fields)
        if result.get('mail_message_id'):
            mail_message_id = self.env['mail.message'].browse(result['mail_message_id'])
            result['last_updated_on'] = mail_message_id.history_line[0].create_date if mail_message_id.history_line else False
            result['history_line'] = [(0, 0, {
                'edit_message_log_note_id': history.id,
                'old_body': history.old_body,
                'new_body': history.new_body,
                'create_date': history.create_date,
            }) for history in mail_message_id.history_line]
        return result

    mail_message_id = fields.Many2one(
        'mail.message', 'Mail Message ID',
        readonly=True, required=True
    )
    # content
    date = fields.Datetime('Date', related='mail_message_id.date')
    body = fields.Html(
        'Contents', sanitize_style=True,
        related='mail_message_id.body', readonly=False
    )

    # origin
    email_from = fields.Char('From', related='mail_message_id.email_from')
    author_id = fields.Many2one(
        'res.partner', 'Author',
        related='mail_message_id.author_id'
    )
    history_line = fields.One2many(
        'edit.history', 'edit_message_log_note_id',
        string='History Lines', copy=True, auto_join=True
    )
    last_updated_on = fields.Datetime(readonly=True)

    def action_send(self):
        for wizard in self:
            message = wizard.mail_message_id
            record = self.env[message.model].browse(message.res_id) if message.is_thread_message() else self.env['mail.thread']

            email_partners_data = []
            for pid, cid, active, pshare, ctype, notif, groups in self.env['mail.followers']._get_recipient_data(None, 'comment', False, pids=message.notified_partner_ids.ids):
                if pid and notif == 'email' or not notif:
                    pdata = {'id': pid, 'share': pshare, 'active': active, 'notif': 'email', 'groups': groups or []}
                    if not pshare and notif:  # has an user and is not shared, is therefore user
                        email_partners_data.append(dict(pdata, type='user'))
                    elif pshare and notif:  # has an user and is shared, is therefore portal
                        email_partners_data.append(dict(pdata, type='portal'))
                    else:  # has no user, is therefore customer
                        email_partners_data.append(dict(pdata, type='customer'))

            record._notify_record_by_email(message, {'partners': email_partners_data}, check_existing=True, send_after_commit=False)
        return {'type': 'ir.actions.act_window_close'}
