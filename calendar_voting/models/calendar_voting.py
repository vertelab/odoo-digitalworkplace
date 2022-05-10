from odoo import fields, models


class CalendarEvent(models.Model):
    _inherit='calendar.event'

    voting_checkbox = fields.Boolean(string="Voting")
