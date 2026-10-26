from odoo import _, api, models


class SlideChannel(models.Model):
    """Bridge the Immich onboarding course to the Immich configuration.

    The course teaches how to fill in the Immich settings. This model does not
    own those settings — they live in ``ir.config_parameter`` and are managed by
    ``website_immich`` (``res.config.settings``). It only provides a guarded
    shortcut so the course's first lesson is one click away from the form it
    talks about.
    """

    _inherit = 'slide.channel'

    @api.model
    def action_open_immich_settings(self):
        """Open the Immich settings block for users allowed to edit it.

        Mirrors the guard in ``website_immich.models.res_users``
        (``_can_manage_immich_settings``) so a user without rights gets a
        readable notification instead of a settings form they cannot save.
        """
        if not self.env.user._can_manage_immich_settings():
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _("Not allowed"),
                    'message': _(
                        "Only administrators and website editors can change "
                        "the Immich connection. Ask one of them to set it up."
                    ),
                    'type': 'warning',
                    'sticky': False,
                },
            }
        return {
            'type': 'ir.actions.act_window',
            'name': _("General Settings"),
            'res_model': 'res.config.settings',
            'view_mode': 'form',
            'target': 'inline',
            'context': {'module': 'website_immich'},
        }
