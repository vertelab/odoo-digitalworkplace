from datetime import datetime
from odoo import models, api, fields

class Content(models.Model):
    _name = 'readit.content'
    _description = 'Readit post and comment content'

    content = fields.Text(string='Content')
    name = fields.Char(string='Author', compute='_getName')
    super_id = fields.Integer(string='Comment/Post ID', readonly=True)

    @api.model
    def _selection_target_model(self):
        return [
            ('readit.comments', 'Comments'), 
            ('readit.posts', 'Posts')
        ]

    model_name = fields.Char(string='Model', readonly=True, store=True)

    super_ref = fields.Reference(
        string='Comment or Post', 
        selection='_selection_target_model', 
        inverse='_set_resource_ref',
        required=True
    )

    def _set_resource_ref(self):
        for s in self:
            if s.super_ref:
                s.super_id = s.super_ref.id

    @api.depends('super_id')
    def _getName(self):
        for s in self:
            if s.super_id:
                if type(s.super_ref) == type(self.env['readit.posts']):
                    s.name = self.env['readit.posts'].search([['id', '=', s.super_id]]).author_id.name
                else:
                    s.name = self.env['readit.comments'].search([['id', '=', s.super_id]]).author_id.name
            else:
                s.name = 'Unknown'