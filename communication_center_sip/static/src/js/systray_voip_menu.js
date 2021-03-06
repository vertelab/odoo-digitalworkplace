odoo.define('communication_center_sip.SystrayVoipMenu', function (require) {
"use strict";

const core = require('web.core');
const config = require('web.config');
const session = require('web.session');
const SystrayMenu = require('web.SystrayMenu');
const Widget = require('web.Widget');

const SystrayVoipMenu = Widget.extend({
    name: 'communication_center_sip',
    template: 'communication_center_sip.switch_panel_top_button',
    events: {
        'click': '_onClick',
    },

    // TODO remove and replace with session_info mechanism
    /**
     * @override
     */
    async willStart() {
        const _super = this._super.bind(this, ...arguments); // limitation of class.js
        const isEmployee = await session.user_has_group('base.group_user');
        if (!isEmployee) {
            return Promise.reject();
        }
        return _super();
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {MouseEvent} ev
     */
    _onClick(ev) {
        ev.preventDefault();
        core.bus.trigger('voip_onToggleDisplay');
    },
});

// Insert the Voip widget button in the systray menu
SystrayMenu.Items.push(SystrayVoipMenu);

return SystrayVoipMenu;

});
