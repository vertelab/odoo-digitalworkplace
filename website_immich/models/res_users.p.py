from odoo import models


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _can_manage_immich_settings(self):
        self.ensure_one()
        return (self.sudo().has_group('base.group_erp_manager')
                or self.sudo().has_group('website.group_website_restricted_editor'))
