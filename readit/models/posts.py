from odoo import models, api, fields, exceptions

class Posts(models.Model):
    _name = 'readit.posts'
    _description = 'A post within a Readit forum subject.'

    name = fields.Char(string='Title', required=True)
    
    def _default_author(self):
        return self.env.user.partner_id

    forum_id = fields.Many2one(comodel_name='readit.forums', string='Forum ID', ondelete='cascade', required=True)
    author_id = fields.Many2one(comodel_name='res.partner', string='Author', ondelete='cascade', readonly=True, default=_default_author)
    content_id = fields.One2many(comodel_name='readit.content', inverse_name='super_id', string='Content', ondelete='cascade', readonly=True)
    comments = fields.One2many(comodel_name='readit.comments', inverse_name='post_id', string='Comments', ondelete='cascade', readonly=True)

    title = fields.Char(string='Title', compute='_getForum')
    total_comments = fields.Integer(string='Total Comments', compute='_totalComments')

    @api.depends('comments')
    def _totalComments(self):
        for s in self:
            if s.comments:
                s.total_comments = len(s.comments)
            else:
                s.total_comments = 0

    @api.depends('forum_id', 'name')
    def _getForum(self):
        for s in self:
            if s.forum_id and s.name:
                s.title = s.forum_id.name + ' > ' + s.name
            elif s.name:
                s.title = 'Unknown > ' + s.name
            else:
                s.title = 'Unknown > Untitled'

    @api.constrains('forum_id')
    def _check_forum(self):
        for s in self:
            if self.env.user.partner_id.id == s.author_id.id:
                print('Valid user:')
                print(self.env.user.partner_id)
            else:
                raise exceptions.ValidationError('User does not own this post!')
    
    @api.constrains('name')
    def _check_title(self):
        for s in self:
            if self.env.user.partner_id.id == s.author_id.id:
                print('Valid user:')
                print(self.env.user.partner_id)
            else:
                raise exceptions.ValidationError('User does not own this post!')
    
    # @override
    def unlink(self):
        for s in self:
            if self.env.user.partner_id.id == s.author_id.id:
                for c in s.content_id:
                    c.unlink()

                for c in s.comments:
                    for t in c.content_id:
                        t.unlink()
                    c.unlink()

                super(Posts, self).unlink()
            else:
                raise exceptions.ValidationError('User does not own this post!')
