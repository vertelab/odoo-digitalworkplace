
import base64
import logging
import re
from uuid import uuid4

from odoo import _, api, fields, models, modules, tools
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.tools import ormcache, formataddr
from odoo.exceptions import AccessError
from odoo.addons.base.models.ir_model import MODULE_UNINSTALL_FLAG


class Channel(models.Model):
    """ A mail.channel is a discussion group that may behave like a listener
    on documents. """
    _inherit = 'mail.channel'

    def channel_info(self, extra_info=False):
        """ Get the informations header for the current channels
            :returns a list of channels values
            :rtype : list(dict)
        """
        if not self:
            return []
        channel_infos = []
        # all relations partner_channel on those channels
        all_partner_channel = self.env['mail.channel.partner'].search([('channel_id', 'in', self.ids)])

        # all partner infos on those channels
        channel_dict = {channel.id: channel for channel in self}
        all_partners = all_partner_channel.mapped('partner_id')
        direct_channel_partners = all_partner_channel.filtered(lambda pc: channel_dict[pc.channel_id.id].channel_type == 'chat')
        direct_partners = direct_channel_partners.mapped('partner_id')
        partner_infos = self.partner_info(all_partners, direct_partners)
        channel_last_message_ids = dict((r['id'], r['message_id']) for r in self._channel_last_message_ids())

        for channel in self:
            info = {
                'id': channel.id,
                'name': channel.name,
                'uuid': channel.uuid,
                'state': 'open',
                'is_minimized': False,
                'channel_type': channel.channel_type,
                'public': channel.public,
                'mass_mailing': channel.email_send,
                'moderation': channel.moderation,
                'is_moderator': self.env.uid in channel.moderator_ids.ids,
                'group_based_subscription': bool(channel.group_ids),
                'create_uid': channel.create_uid.id,
                'members': [partners for partners in partner_infos.values()]
            }
            if extra_info:
                info['info'] = extra_info

            # add last message preview (only used in mobile)
            info['last_message_id'] = channel_last_message_ids.get(channel.id, False)
            # listeners of the channel
            channel_partners = all_partner_channel.filtered(lambda pc: channel.id == pc.channel_id.id)

            # find the channel partner state, if logged user
            if self.env.user and self.env.user.partner_id:
                # add needaction and unread counter, since the user is logged
                info['message_needaction_counter'] = channel.message_needaction_counter
                info['message_unread_counter'] = channel.message_unread_counter

                # add user session state, if available and if user is logged
                partner_channel = channel_partners.filtered(lambda pc: pc.partner_id.id == self.env.user.partner_id.id)
                if partner_channel:
                    partner_channel = partner_channel[0]
                    info['state'] = partner_channel.fold_state or 'open'
                    info['is_minimized'] = partner_channel.is_minimized
                    info['seen_message_id'] = partner_channel.seen_message_id.id
                    info['custom_channel_name'] = partner_channel.custom_channel_name
                    info['is_pinned'] = partner_channel.is_pinned

            # add members infos
            if channel.channel_type != 'channel':
                # avoid sending potentially a lot of members for big channels
                # exclude chat and other small channels from this optimization because they are
                # assumed to be smaller and it's important to know the member list for them
                info['members'] = [channel._channel_info_format_member(partner, partner_infos[partner.id]) for partner in channel_partners.partner_id.sudo().with_prefetch(all_partners.ids)]
            if channel.channel_type != 'channel':
                info['seen_partners_info'] = [{
                    'id': cp.id,
                    'partner_id': cp.partner_id.id,
                    'fetched_message_id': cp.fetched_message_id.id,
                    'seen_message_id': cp.seen_message_id.id,
                } for cp in channel_partners]

            channel_infos.append(info)
        return channel_infos
