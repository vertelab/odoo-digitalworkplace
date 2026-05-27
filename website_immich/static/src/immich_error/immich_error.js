import { Component } from "@odoo/owl";
import { ImmichCredentials } from "../immich_credentials/immich_credentials";

export class ImmichError extends Component {
    static template = "website_immich.ImmichError";
    static components = {
        ImmichCredentials,
    };
    static props = {
        title: String,
        subtitle: String,
        showCredentials: Boolean,
        submitCredentials: { type: Function, optional: true },
        hasCredentialsError: { type: Boolean, optional: true },
    };
}
