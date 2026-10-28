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
 * layer was removed from the web addon (only `legacy/js/core/class.js`,
 * `legacy/js/libs/jquery.js` and `legacy/js/public/*` remain), and clipboard
 * access now goes through the native `navigator.clipboard` API wrapped by
 * `@web/core/copy_button/copy_button`.
 *
 * The widget is only meaningful in read-only mode; in edit mode the backend
 * falls back to the standard char field.
 */
export class CopyToClipboardUrlField extends Component {
    static template = "user_settings_dav.CopyToClipboardUrlField";
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
    // The DOM structure is identical in read and edit mode: a link plus an
    // icon. There is nothing to edit, so keep it out of the edit-mode cycle.
    isEmpty: () => false,
    extractProps: () => ({}),
};

registry.category("fields").add("copy_to_clipbord_url", copyToClipboardUrlField);
