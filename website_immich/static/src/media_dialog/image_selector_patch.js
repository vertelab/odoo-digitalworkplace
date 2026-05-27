import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { KeepLast } from "@web/core/utils/concurrency";
import { rpc } from "@web/core/network/rpc";
import { useService } from "@web/core/utils/hooks";
import { ImageSelector } from "@html_editor/main/media/media_dialog/image_selector";

import { ImmichError } from "../immich_error/immich_error";
import { useState } from "@odoo/owl";

patch(ImageSelector.prototype, {
    setup() {
        super.setup();
        this.immich = useService("immich");
        this.keepLastImmich = new KeepLast();
        this.immichState = useState({
            immichRecords: [],
            isFetchingImmich: false,
            isMaxed: false,
            immichError: null,
            useImmich: true,
        });

        this.NUMBER_OF_RECORDS_TO_DISPLAY = 30;

        this.errorMessages = {
            config_not_found: {
                title: _t("Setup Immich to access your photo library."),
                subtitle: "",
            },
            401: {
                title: _t("Unauthorized"),
                subtitle: _t("Please check your Immich API key."),
            },
            connection_error: {
                title: _t("Connection Error"),
                subtitle: _t("Could not connect to the Immich server. Please check the URL."),
            },
            timeout: {
                title: _t("Timeout"),
                subtitle: _t("The request to the Immich server timed out."),
            },
        };
    },

    get canLoadMore() {
        if (this.state.searchService === "all") {
            return (
                super.canLoadMore ||
                (this.state.needle &&
                    !this.immichState.isMaxed &&
                    !this.immichState.immichError)
            );
        } else if (this.state.searchService === "immich") {
            return (
                this.state.needle &&
                !this.immichState.isMaxed &&
                !this.immichState.immichError
            );
        }
        return super.canLoadMore;
    },

    get hasContent() {
        if (this.state.searchService === "all") {
            return super.hasContent || !!this.immichState.immichRecords.length;
        } else if (this.state.searchService === "immich") {
            return !!this.immichState.immichRecords.length;
        }
        return super.hasContent;
    },

    get errorTitle() {
        if (this.errorMessages[this.immichState.immichError]) {
            return this.errorMessages[this.immichState.immichError].title;
        }
        return _t("Something went wrong");
    },

    get errorSubtitle() {
        if (this.errorMessages[this.immichState.immichError]) {
            return this.errorMessages[this.immichState.immichError].subtitle;
        }
        return _t("Please check your internet connection or contact administrator.");
    },

    get selectedRecordIds() {
        return this.props.selectedMedia[this.props.id]
            .filter((media) => media.mediaType === "immichRecord")
            .map(({ id }) => id);
    },

    get isFetching() {
        return super.isFetching || this.immichState.isFetchingImmich;
    },

    get combinedRecords() {
        function alternate(a, b) {
            return [a.map((v, i) => (i < b.length ? [v, b[i]] : v)), b.slice(a.length)].flat(2);
        }
        return alternate(this.immichState.immichRecords, this.state.libraryMedia);
    },

    get allAttachments() {
        return [...super.allAttachments, ...this.immichState.immichRecords];
    },

    async fetchImmichRecords(offset) {
        if (!this.state.needle) {
            return { records: [], isMaxed: false };
        }
        this.immichState.isFetchingImmich = true;
        try {
            const { isMaxed, images } = await this.immich.getImages(
                this.state.needle,
                offset,
                this.NUMBER_OF_RECORDS_TO_DISPLAY,
                this.props.orientation
            );
            this.immichState.isFetchingImmich = false;
            this.immichState.immichError = false;
            const existingIds = new Set(this.immichState.immichRecords.map(r => r.id));
            const newImages = images.filter(record => {
                if (existingIds.has(record.id)) {
                    return false;
                }
                existingIds.add(record.id);
                return true;
            });
            const records = newImages.map((record) => {
                return Object.assign({}, record, {
                    url: record.url,
                    mediaType: "immichRecord",
                });
            });
            return { isMaxed, records };
        } catch (e) {
            this.immichState.isFetchingImmich = false;
            if (e === "no_access") {
                this.immichState.useImmich = false;
            } else {
                this.immichState.immichError = e;
            }
            return { records: [], isMaxed: true };
        }
    },

    async loadMore(...args) {
        await super.loadMore(...args);
        return this.keepLastImmich
            .add(this.fetchImmichRecords(this.immichState.immichRecords.length))
            .then(({ records, isMaxed }) => {
                this.immichState.immichRecords.push(...records);
                this.immichState.isMaxed = isMaxed;
            });
    },

    async search(...args) {
        await super.search(...args);
        await this.searchImmich();
    },

    async searchImmich() {
        if (!this.state.needle) {
            this.immichState.immichError = false;
            this.immichState.immichRecords = [];
            this.immichState.isMaxed = false;
        }
        return this.keepLastImmich
            .add(this.fetchImmichRecords(0))
            .then(({ records, isMaxed }) => {
                this.immichState.immichRecords = records;
                this.immichState.isMaxed = isMaxed;
            });
    },

    async onClickRecord(media) {
        this.props.selectMedia({ ...media, mediaType: "immichRecord", query: this.state.needle });
        if (!this.props.multiSelect) {
            await this.props.save();
        }
    },

    async submitCredentials(url, apiKey) {
        this.immichState.immichError = null;
        await rpc("/website_immich/save_config", { url, api_key: apiKey });
        await this.searchImmich();
    },
});

ImageSelector.components = {
    ...ImageSelector.components,
    ImmichError,
};
