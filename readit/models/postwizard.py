# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

class PostWizard(models.TransientModel):

    _name = 'readit.postwizard'
    _description = 'Wizard: create content for a post'

    def _default_post(self):
        return self.env['readit.posts'].browse(self._context.get('active_id'))

    @api.model
    def _selection_target_model(self):
        return [('readit.posts', 'Posts')]
    
    content = fields.Text(string='Text')
    name = fields.Char(string='Author', compute='_getName')
    model_name = fields.Char(string='Model', readonly=True, store=True)
    super_id = fields.Many2one(comodel_name='readit.posts', string='Post', required=True, default=_default_post, readonly=True)

    super_ref = fields.Char(string='Post', readonly=True)


    @api.depends('super_id')
    def _getName(self):
        self.ensure_one()
        if self.super_id:
            self.name = self.super_id.author_id.name
        else:
            self.name = 'Unknown'

    def add_content(self):
        self.ensure_one()
        if self.super_id.author_id != self.env.user.partner_id:
            raise exceptions.ValidationError('User does not own this post!')
        
        if self.super_ref:
            print(self.super_ref)
        else:
            id = int(self.super_id.id)
            self.super_ref = 'readit.posts,' + str(id)

        self.env['readit.content'].create({
            'super_id': self.super_id.id,
            'model_name': self.model_name,
            'super_ref': self.super_ref,
            'content': self.content,
            'name': self.name,
        })