import { registry } from "@web/core/registry";
import { Component, onWillDestroy } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

/**
 * Boolean field widget toggling whether a record is in the call queue.
 *
 * Odoo 18 port: the previous implementation extended `web.AbstractField`,
 * used `this._rpc`, `this.trigger_up('reload')` and subscribed to
 * `core.bus.on('voip_widget_refresh')`. None of those exist in the OWL
 * component layer:
 *   - `this.env.services.orm.call(...)` replaces `this._rpc`
 *   - `record.load()` on the model replaces `trigger_up('reload')`
 *   - the event bus is imported directly and unsubscribed on destroy
 */
export class CallCenterField extends Component {
    static template = "communication_center_sip.CallCenterField";
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.bus = this.env.bus;

        this.onVoipRefresh = (resID) => {
            if (resID !== this.props.record.resId) {
                return;
            }
            this.props.record.load();
        };
        this.bus.addEventListener("voip_widget_refresh", this.onVoipRefresh);
        onWillDestroy(() => {
            this.bus.removeEventListener("voip_widget_refresh", this.onVoipRefresh);
        });
    }

    get isInCallQueue() {
        return Boolean(this.props.record.data[this.props.name]);
    }

    get helper() {
        return this.isInCallQueue ? "Remove from Call Queue" : "Add to Call Queue";
    }

    get icon() {
        return this.isInCallQueue
            ? "fa-minus text-danger"
            : "fa-plus text-success";
    }

    async onClick(ev) {
        ev.stopPropagation();
        ev.preventDefault();
        const model = this.props.record.resModel;
        const resId = this.props.record.resId;
        await this.orm.call(
            model,
            this.isInCallQueue ? "delete_call_in_queue" : "create_call_in_queue",
            [[resId]]
        );
        await this.props.record.load();
    }
}

export const callCenterField = {
    component: CallCenterField,
    displayName: "Call center",
    supportedTypes: ["boolean"],
};

registry.category("fields").add("call_center", callCenterField);
