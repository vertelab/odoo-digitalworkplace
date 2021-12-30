from odoo import models, api, fields

class Comments(models.Model):
    _name = 'readit.comments'
    _description = 'A comment about a post from a Readit forum subject.'
    _sequence = 'readit_posts_id_seq'

    name = fields.Char(string='Author', compute='_getAuthor')

    post_id = fields.Many2one(comodel_name='readit.posts', string='Post', ondelete='cascade', required=True)
    author_id = fields.Many2one(comodel_name='res.partner', string='Author', ondelete='cascade', readonly=True)
    content_id = fields.One2many(comodel_name='readit.content', inverse_name='super_id', string='Content', ondelete='cascade', readonly=True)
    
    @api.depends('author_id')
    def _getAuthor(self):
        for s in self:
            if s.author_id:
                s.name = s.author_id.name
            else:
                s.name = 'Unknown'