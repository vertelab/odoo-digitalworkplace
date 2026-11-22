import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { CopyButton } from "@web/core/copy_button/copy_button";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

/**
 * Read-only field widget that renders a URL as a link together with a
 * "copy to clipboard" icon.
 *
 * Odoo 18 port: the previous implementation extended the legacy
 * `web.AbstractField` and used ClipboardJS. Both are gone — the legacy field
 * layer was removed from the web addon, and clipboard access now goes through
 * the native `navigator.clipboard` API wrapped by
 * `@web/core/copy_button/copy_button`.
 *
 * The widget is only meaningful in read-only mode; there is nothing to edit.
 */
export class CopyToClipboardUrlField extends Component {
    static template = "calendar_voting.CopyToClipboardUrlField";
    static components = { CopyButton };
    static props = {
        ...standardFieldProps,
    };

    get url() {
        return (this.props.record.data[this.props.name] || "").trim();
    }
}

export const copyToClipboardUrlField = {
    component: CopyToClipboardUrlField,
    displayName: "Copy to clipboard URL",
    supportedTypes: ["char"],
    isEmpty: () => false,
};

registry.category("fields").add("copy_to_clipbord_url", copyToClipboardUrlField);
