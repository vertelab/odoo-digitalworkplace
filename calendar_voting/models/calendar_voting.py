from calendar import calendar
from venv import create
from odoo import _, fields, models, api
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CalendarEvent(models.Model):
    _inherit='calendar.event'

    voting_checkbox = fields.Boolean(string="Voting")
    participant_ids = fields.One2many(comodel_name="calendar.voting", inverse_name="event_id")
    choose_day = fields.Selection(
        selection=[('monday', 'Monday'), 
        ('tuesday', 'Tuesday'), 
        ('wednesday', 'Wednesday'), 
        ('thursday', 'Thursday'), 
        ('friday', 'Friday')]
    )
    choose_this_day = fields.Boolean()

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
            record.choose_a_day(vals)
        return res

    def choose_a_day(self):
        for record in self:
            voting_admin = record.user_id
            if (record.choose_this_day == True) and (voting_admin == self.env.user):
                if record.choose_day != False:
                    _logger.error(f"YYYEEEEESSSSS")
                    #TODO create a funktion for turning off the voting
                elif record.choose_day == False:
                    raise UserError(_("Pleas choose a day for the meeting to end the voting"))
                else:
                    break
            elif  (record.choose_day != False) and (voting_admin != self.env.user):
                    raise UserError(_("You are not allowed to choose day exept for voting admin!"))
            else:
                break

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
            # elif record.choose_this_day == True:
            #     raise UserError(_("The voting is over, you are not allowed to vote anymore!"))
        res = super().write(vals)
        return res


    #TODO: *create an admin for the metting(the user that created the metting(
    # *find the id of how created the meeting and compare it to admins id(
    # *might be able to use name?(
    # *ansvarig for the meeting?)))),
    # *create a selector,
    # *admin can deside witch day the metting will be at from selector/drop down menu, 
    # and when the day is desided by admin the metting will be over and 
    # move to that day in the calendar.
    # use date & date range widget(uvenacc event?) to move meeting maby

