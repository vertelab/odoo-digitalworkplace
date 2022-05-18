from odoo import fields, models


class CalendarEvent(models.Model):
    _inherit='calendar.event'

    voting_checkbox = fields.Boolean(string="Voting")
    partisipants_ids = fields.One2many(comodel_name="calendar.test", inverse_name="test")

class CalendarTest(models.Model):
    _name='calendar.test'

    test = fields.Many2one(comodel_name="calendar.event")
    Name = fields.Text()
    Monday = fields.Boolean()
    Tuesday= fields.Boolean()
    Wednesday = fields.Boolean()
    Thursday = fields.Boolean()
    Friday = fields.Boolean()