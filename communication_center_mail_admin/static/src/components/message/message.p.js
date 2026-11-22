/* See LICENSE file for full copyright and licensing details. */

odoo.define('communication_center_mail_admin/static/src/components/message/message.js', function (require) {
    "use strict";

    const components = {
        Message: require('mail/static/src/components/message/message.js'),
    };

    const { patch } = require('web.utils');
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var _t = core._t;

    var QWeb = core.qweb;
    var rpc = require('web.rpc');


    patch(components.Message, 'communication_center_mail_admin/static/src/components/message/message.js', {

        /**
         * @private
         * @param {MouseEvent} ev
         */
        _onWkClickEdit(ev) {
            ev.stopPropagation();
            this.message.wkEdit();
        },

        /**
         * @private
         * @param {MouseEvent} ev
         */
        _onWkClickDelete(ev) {
            ev.stopPropagation();
            var self = this;
            Dialog.confirm(
                self,
                _t("Are you sure you want to delete this message? This action can't be undone."), {
                    title: _t("Warning"),
                    confirm_callback: function () {
                        self.message.wkDelete();
                    },
                }
            );
        },

        _onClickCreateAction(ev) {
            ev.stopPropagation();
            let self = this;
            const record_details = this.message.originThread.localId.split('_')

            rpc.query({
                model: 'ir.model',
                method: 'search',
                args: [[["model", "=", record_details[1]]]],
            }).then(function (data) {
                const action = {
                    type: 'ir.actions.act_window',
                    name: self.env._t("Schedule Activity"),
                    res_model: 'mail.activity',
                    view_mode: 'form',
                    views: [[false, 'form']],
                    target: 'new',
                    context: {
                        default_res_model_id: data[0] ,
                        default_res_id: record_details[2] ,
                        default_note: self.message.body,
                    },
                };
                return self.env.bus.trigger('do-action', {
                    action,
                    options: {
                        on_close: () => {
                            self.trigger('reload', { keepChanges: true });
                        },
                    },
                });

            });
        },

        _onClickMarkUnread(ev) {
            ev.stopPropagation();
        }
    });

});
