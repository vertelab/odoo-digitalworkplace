# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields

# Add 'sip_password' field to the private fields.
# Only users who can modify the res_user (incl. the user himself) see the private fields real content
# #if VERSION <= "18.0"
# USER_PRIVATE_FIELDS was removed in 19.0; SELF_READABLE_FIELDS (below) is
# the list that decides what a user may read on their own record.
from odoo.addons.base.models import res_users
res_users.USER_PRIVATE_FIELDS.append('sip_password')
# #endif


class ResUsers(models.Model):
    _inherit = 'res.users'

    # #if VERSION <= "18.0"
    def __init__(self, pool, cr):
        """ Override of __init__ to add access rights.
            Access rights are disabled by default, but allowed
            on some specific fields defined in self.SELF_{READ/WRITE}ABLE_FIELDS.
        """
        init_res = super(ResUsers, self).__init__(pool, cr)
        voip_fields = [
            'sip_login',
            'sip_password',
            'sip_external_phone',
            'sip_always_transfer',
            'sip_ignore_incoming',
            'mobile_call_method',
        ]
        # duplicate list to avoid modifying the original reference
        type(self).SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        type(self).SELF_WRITEABLE_FIELDS.extend(voip_fields)
        # duplicate list to avoid modifying the original reference
        type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        type(self).SELF_READABLE_FIELDS.extend(voip_fields)
        return init_res
    # #else
    # SELF_READABLE_FIELDS/SELF_WRITEABLE_FIELDS are properties in 19.0;
    # assigning to them on the class no longer works.
    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + [
            'sip_login',
            'sip_password',
            'sip_external_phone',
            'sip_always_transfer',
            'sip_ignore_incoming',
            'mobile_call_method',
        ]

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + [
            'sip_login',
            'sip_password',
            'sip_external_phone',
            'sip_always_transfer',
            'sip_ignore_incoming',
            'mobile_call_method',
        ]
    # #endif

    mobile_call_method = fields.Selection(
        [('ask', 'Ask'), ('voip', 'Voip'), ('phone', 'Phone')],
        string="Mobile call",
        groups="base.group_user",
        default='ask',
        required=True,
        help="""Method to use to made a call on mobile:
        * VoIP: Always used as a softphone
        * Phone: Always use the device's phone
        * Ask: Always prompt""")
    sip_login = fields.Char("SIP Login / Browser's Extension", groups="base.group_user")
    sip_password = fields.Char('SIP Password', groups="base.group_user")
    sip_external_phone = fields.Char("Handset Extension", groups="base.group_user")
    sip_always_transfer = fields.Boolean("Always Redirect to Handset", default=False,
                                         groups="base.group_user")
    sip_ignore_incoming = fields.Boolean("Reject All Incoming Calls", default=False,
                                         groups="base.group_user")

    last_seen_phone_call = fields.Many2one('voip.phonecall')

    @api.model
    def reset_last_seen_phone_call(self):
        domain = [
            ('user_id', '=', self.env.user.id),
            ('call_date', '!=', False),
            ('in_queue', '=', True),
        ]
        last_call = self.env['voip.phonecall'].search(domain, order='call_date desc', limit=1)
        self.env.user.last_seen_phone_call = last_call.id
