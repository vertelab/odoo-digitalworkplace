import { Component, useState } from "@odoo/owl";

export class ImmichCredentials extends Component {
    static template = "website_immich.ImmichCredentials";
    static props = {
        submitCredentials: Function,
        hasCredentialsError: Boolean,
    };
    setup() {
        this.state = useState({
            url: "",
            api_key: "",
            hasUrlError: this.props.hasCredentialsError,
            hasKeyError: this.props.hasCredentialsError,
        });
    }

    submitCredentials() {
        if (this.state.url === "") {
            this.state.hasUrlError = true;
        } else if (this.state.api_key === "") {
            this.state.hasKeyError = true;
        } else {
            this.props.submitCredentials(this.state.url, this.state.api_key);
        }
    }
}
