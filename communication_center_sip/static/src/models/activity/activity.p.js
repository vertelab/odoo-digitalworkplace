odoo.define('communication_center_sip/static/src/models/activity/activity.js', function (require) {
    'use strict';

    const {
        registerClassPatchModel,
        registerFieldPatchModel,
        registerInstancePatchModel,
    } = require('mail/static/src/model/model_core.js');
    const { attr } = require('mail/static/src/model/model_field.js');

    registerClassPatchModel('mail.activity', 'communication_center_sip/static/src/models/activity/activity.js', {
        //----------------------------------------------------------------------
        // Public
        //----------------------------------------------------------------------

        /**
         * @override
         */
        convertData(data) {
            const data2 = this._super(data);
            if ('phone' in data) {
                data2.phone = data.phone;
            }
            return data2;
        },
    });

    registerFieldPatchModel('mail.activity', 'communication_center_sip/static/src/models/activity/activity.js', {
        phone: attr(),
    });

    registerInstancePatchModel('mail.activity', 'communication_center_sip/static/src/models/activity/activity.js', {

        /**
         * @override
         */
        _created() {
            const res = this._super(...arguments);
            this.env.bus.on('voip_reload_chatter', this, this._onReloadChatter);
            return res;
        },
        /**
         * @override
         */
        _willDelete() {
            this.env.bus.off('voip_reload_chatter', this, this._onReloadChatter);
            return this._super(...arguments);
        },

        //----------------------------------------------------------------------
        // Handlers
        //----------------------------------------------------------------------

        /**
         * @private
         */
        _onReloadChatter() {
            this.thread.refreshActivities();
        },
    });

});
