# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CommentWizard(models.TransientModel):

    _name = 'readit.commentwizard'
    _description = 'Wizard: create a comment with content'

    def _default_post(self):
        return self.env['readit.posts'].browse(self._context.get('active_id'))

    def _default_author(self):
        return self.env.user.partner_id 

    @api.model
    def _selection_target_model(self):
        return [('readit.comments', 'Comments')]

    comment_name = fields.Char(string='Author', compute='_getName')
    post_id = fields.Integer(string='Post', default=_default_post, readonly=True)
    author_id = fields.Integer(string='Author', default=_default_author, readonly=True)
    
    content = fields.Text(string='Text')
    content_name = fields.Char(string='Author', compute='_getName')
    model_name = fields.Char(string='Model', readonly=True, store=True)
    super_id = fields.Integer(string='Comment ID', readonly=True)
    super_ref = fields.Char(string='Comment', readonly=True)

    @api.depends('author_id')
    def _getName(self):
        self.ensure_one()
        if self.author_id:
            self.content_name = self.env.user.name
            self.comment_name = self.env.user.name
        else:
            self.content_name = 'Unknown'
            self.comment_name = 'Unknown'

    def add_comment(self):
        self.ensure_one()
        ret = self.env['readit.comments'].create([{
            'name': self.comment_name,
            'author_id': self.author_id,
            'post_id': self.post_id,
        }])

        self.super_id = ret.id
        if self.super_ref:
            print(self.super_ref)
        else:
            id = int(self.super_id)
            self.super_ref = 'readit.comments,' + str(id)

        if self.super_id:
            self.env['readit.content'].create({
                'super_id': self.super_id,
                'model_name': self.model_name,
                'super_ref': self.super_ref,
                'content': self.content,
                'name': self.content_name,
            })