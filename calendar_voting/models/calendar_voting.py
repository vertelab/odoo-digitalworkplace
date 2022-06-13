from calendar import calendar
from email.policy import default
from venv import create
from numpy import choose
from odoo import _, fields, models, api
import logging
from odoo.exceptions import UserError
from datetime import datetime, date
from odoo.tools import pycompat

_logger = logging.getLogger("\033[100m"+__name__+"\033[0m")



class CalendarEvent(models.Model):
    _inherit='calendar.event'

    voting_checkbox = fields.Boolean(string="Voting")
    participant_ids = fields.One2many(comodel_name="calendar.voting", inverse_name="event_id")
    
    choose_this_day = fields.Boolean()
    is_voting_admin = fields.Boolean(compute="_compute_voting_off")
    choose_day_calendar = fields.Date()
    showtime = fields.Char(compute="_compute_showtime")

    @api.depends("is_voting_admin", "user_id")
    def _compute_voting_off(self):
        for record in self:
            voting_admin = record.user_id
            record.is_voting_admin = voting_admin == self.env.user

    @api.depends("start")
    def _compute_showtime (self):
        timezone = self._context.get('tz') or self.env.user.partner_id.tz or 'UTC'
        self_tz = self.with_context(tz=timezone)
        for record in self:
            date = fields.Datetime.context_timestamp(self_tz, fields.Datetime.from_string(record.start))
            record.showtime = pycompat.to_text(date.strftime('%H:%M:%S'))

    def create_participants(self, partners):
        for partner in partners:
            self.env['calendar.voting'].create({'event_id': self.id, 'partner_id': partner})

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if vals.get("voting_checkbox"):
            if (partners := vals.get("partner_ids")) and len(partners[0][2]) >1:
                _logger.error("sdsadf")
                res.create_participants(partners[0][2])
            else:
                raise UserError(_("Not allowed to create a voting with only yourself, please add another person."))
        res.send_start_mail(vals)
        return res
    
    def send_start_mail(self, vals):
        for record in self:
            if vals.get("voting_checkbox"):
                template = self.env.ref('calendar_voting.calendar_template_voting_invitation')
                for attendee in record.attendee_ids:
                    template.send_mail(attendee.id)

    def write(self, vals):
        if "voting_checkbox" in vals or "choose_this_day" in vals:
            for record in self:
                if not self.env.user == record.user_id:
                    raise UserError(_("STOP HACKING!"))
        if "choose_day_calendar" in vals:
            for record in self:
                time_save = record.start.strftime("%H:%M:%S")
                vals["start"] = vals["choose_day_calendar"]+ " "+time_save

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
            record.choose_a_day(vals)
        return res

    def choose_a_day(self, vals):
        for record in self:
            voting_admin = record.user_id
            if (record.choose_this_day) and (voting_admin == self.env.user):
                if record.choose_day_calendar:
                    record.send_end_mail(vals)
                elif not record.choose_day_calendar:
                    raise UserError(_("Pleas choose a day for the meeting to end the voting"))

    def send_end_mail(self, vals):
        for record in self:
            if vals.get("choose_this_day"):
                if record.choose_day_calendar:
                    template = self.env.ref('calendar_voting.calendar_template_voting_ended')
                    for attendee in record.attendee_ids:
                        template.send_mail(attendee.id)


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
            if record.event_id.choose_this_day == True:
                raise UserError(_("The voting is over, you are not allowed to vote anymore!"))
            elif record.partner_id != self.env.user.partner_id:
                raise UserError(_("You are not allowed to vote for anyone but yourself!"))
        res = super().write(vals)
        return res

