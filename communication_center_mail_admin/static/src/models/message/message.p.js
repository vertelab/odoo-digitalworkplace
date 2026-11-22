odoo.define('communication_center_mail_admin/static/src/models/message/message.js', function (require) {
    "use strict";

    const {
        registerClassPatchModel,
        registerInstancePatchModel,
        registerFieldPatchModel
    } = require('mail/static/src/model/model_core.js');
    const { attr } = require('mail/static/src/model/model_field.js');
    const { str_to_datetime } = require('web.time');
    const { getLangDatetimeFormat } = require('web.time');
    const { timeFromNow } = require('mail.utils');


    registerClassPatchModel('mail.message', 'communication_center_mail_admin/static/src/models/message/message.js', {
        /**
         * @override
         */
        convertData(data) {
            const data2 = this._super(data);
            if ('wk_edit' in data) {
                data2.wk_edit = data.wk_edit;
            }
            if ('wk_delete' in data) {
                data2.wk_delete = data.wk_delete;
            }
            if ('wk_is_updated' in data) {
                data2.wk_is_updated = data.wk_is_updated;
                if(data2.wk_is_updated){
                    data2.wkDateTime = moment(str_to_datetime(data.wk_last_updated_on)).format(getLangDatetimeFormat());
                }
            }
            if ('wk_last_updated_on' in data && data.wk_last_updated_on) {
                data2.wk_last_updated_on = moment(str_to_datetime(data.wk_last_updated_on));
            }
            return data2;
        },

        /**
         * Refreshes the value of `dateFromNow` field to the "current now".
         */
        refreshDateFromNow() {
            this._super();
            this.update({ wkDateFromNow: this._computeWkDateFromNow() });
        },

    });

    registerInstancePatchModel('mail.message', 'communication_center_mail_admin/static/src/models/message/message.js', {

        /**
         * @returns {string}
         */
        _computeWkDateFromNow() {
            if (!this.wk_last_updated_on) {
                return clear();
            }
            return timeFromNow(this.wk_last_updated_on);
        },

        /**
         * Opens (legacy) form view dialog to edit current message or log note and updates
         * the message or log note when dialog is closed.
         */
         async wkEdit() {
            const data = await this.env.services.rpc({
                model: 'mail.message',
                method: 'checkWkEdit',
                args: [[this.id]],
            });
            if (!data) {
                return;
            }
            this.env.bus.trigger('do-action', {
                action: 'communication_center_mail_admin.edit_message_log_note_action',
                options: {
                    additional_context: {
                        default_mail_message_id: this.id,
                    },
                    on_close: () => {
                        this.fetchAndUpdate();
                    },
                },
            });
         },

        async fetchAndUpdate() {
            const [data] = await this.async(() => this.env.services.rpc({
                model: 'mail.message',
                method: 'edit_message_format',
                args: [this.id],
            }, { shadow: true }));
            if (data) {
                this.update(this.constructor.convertData(data));
            }
        },

        /**
        * Delete the record from database and locally.
        */
        async wkDelete() {
            await this.async(() => this.env.services.rpc({
                model: 'mail.message',
                method: 'unlink',
                args: [[this.id]],
                context: {"wkDeleteFlag": true},
            }));
            this.delete();
        },
    });

    registerFieldPatchModel('mail.message', 'communication_center_mail_admin/static/src/models/message/message.js', {
        wk_edit: attr({
            default: false,
        }),
        wk_delete: attr({
            default: false,
        }),
        wk_is_updated: attr({
            default: false,
        }),

        wkDateTime: attr({
            default: moment(),
        }),

        wk_last_updated_on: attr({
            default: moment(),
        }),
        /**
         * States the time elapsed since date up to now.
         */
        wkDateFromNow: attr({
            compute: '_computeWkDateFromNow',
            dependencies: [
                'wk_last_updated_on',
            ],
        }),
    });

});
