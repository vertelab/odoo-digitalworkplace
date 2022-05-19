from calendar import calendar
from odoo import _, fields, models, api
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CalendarEvent(models.Model):
    _inherit='calendar.event'

    voting_checkbox = fields.Boolean(string="Voting")
    participant_ids = fields.One2many(comodel_name="calendar.voting", inverse_name="event_id")

    def create_participants(self, partners):
        for partner in partners:
            self.env['calendar.voting'].create({'event_id': self.id, 'partner_id': partner})

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if vals.get("voting_checkbox"):
            if (partners := vals.get("partner_ids")):
                res.create_participants(partners[0][2])
            else:
                raise UserError(_("Not allowed to create a voting with only yourself, please add another person."))
        return res

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            if (partners := vals.get("partner_ids")):
                to_be_created = list(filter(lambda p: p not in [x.partner_id.id for x in record.participant_ids], partners[0][2]))
                record.create_participants(to_be_created)
        for record in self:
            voting_partners = set(record.participant_ids.partner_id.ids)
            event_partners = set(record.partner_ids.ids)
            if voting_partners != event_partners:
                difference = list(voting_partners - event_partners)
                to_be_removed = record.participant_ids.filtered(lambda p: p.partner_id.id in difference)
                to_be_removed.unlink()
        return res


class CalendarVoting(models.Model):
    _name='calendar.voting'

    event_id = fields.Many2one(comodel_name="calendar.event")
    partner_id = fields.Many2one(comodel_name="res.partner")
    name = fields.Char(related="partner_id.name")
    monday = fields.Boolean()
    tuesday= fields.Boolean()
    wednesday = fields.Boolean()
    thursday = fields.Boolean()
    friday = fields.Boolean()

    def write(self, vals):
        for record in self:
            if record.partner_id != self.env.user.partner_id:
                raise UserError(_("You are not allowed to vote for anyone but yourself!"))
        res = super().write(vals)
        return res