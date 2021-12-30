from odoo import models, api, fields

class Forums(models.Model):
    _name = 'readit.forums'
    _description = 'A Readit Forum subject.'

    name = fields.Char(string='Subject', required=True)
    image = fields.Char(string='Image URL')
    description = fields.Char(string='Description')

    _sql_contrainst = [(
        'readit_subject_unique', 
        'UNIQUE(name)', 
        'Each forum subject must be unique!'
    )]