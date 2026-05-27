import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { KeepLast } from "@web/core/utils/concurrency";
import { MediaDialog, TABS } from "@web_editor/components/media_dialog/media_dialog";
import { ImageSelector } from "@web_editor/components/media_dialog/image_selector";
import { rpc } from "@web/core/network/rpc";
import { useService } from "@web/core/utils/hooks";
import { ImmichError } from "../immich_error/immich_error";

patch(ImageSelector.prototype, {
    setup() {
        super.setup();
        this.immich = useService('immich');
        this.keepLastImmich = new KeepLast();

        this.state.immichRecords = [];
        this.state.isFetchingImmich = false;
        this.state.isMaxed = false;
        this.state.immichError = null;
        this.state.useImmich = true;
        this.NUMBER_OF_RECORDS_TO_DISPLAY = 30;

        this.errorMessages = {
            'config_not_found': {
                title: _t("Setup Immich to access your photo library."),
                subtitle: "",
            },
            401: {
                title: _t("Unauthorized"),
                subtitle: _t("Please check your Immich API key."),
            },
            'connection_error': {
                title: _t("Connection Error"),
                subtitle: _t("Could not connect to the Immich server. Please check the URL."),
            },
            'timeout': {
                title: _t("Timeout"),
                subtitle: _t("The request to the Immich server timed out."),
            },
        };
    },

    get canLoadMore() {
        if (this.state.searchService === 'all') {
            return super.canLoadMore || this.state.needle && !this.state.isMaxed && !this.state.immichError;
        } else if (this.state.searchService === 'immich') {
            return this.state.needle && !this.state.isMaxed && !this.state.immichError;
        }
        return super.canLoadMore;
    },

    get hasContent() {
        if (this.state.searchService === 'all') {
            return super.hasContent || !!this.state.immichRecords.length;
        } else if (this.state.searchService === 'immich') {
            return !!this.state.immichRecords.length;
        }
        return super.hasContent;
    },

    get errorTitle() {
        if (this.errorMessages[this.state.immichError]) {
            return this.errorMessages[this.state.immichError].title;
        }
        return _t("Something went wrong");
    },

    get errorSubtitle() {
        if (this.errorMessages[this.state.immichError]) {
            return this.errorMessages[this.state.immichError].subtitle;
        }
        return _t("Please check your internet connection or contact administrator.");
    },

    get selectedRecordIds() {
        return this.props.selectedMedia[this.props.id].filter(media => media.mediaType === 'immichRecord').map(({ id }) => id);
    },

    get isFetching() {
        return super.isFetching || this.state.isFetchingImmich;
    },

    get combinedRecords() {
        function alternate(a, b) {
            return [
                a.map((v, i) => i < b.length ? [v, b[i]] : v),
                b.slice(a.length),
            ].flat(2);
        }
        return alternate(this.state.immichRecords, this.state.libraryMedia);
    },

    get allAttachments() {
        return [...super.allAttachments, ...this.state.immichRecords];
    },

    set canLoadMore(_) {},
    set hasContent(_) {},
    set isFetching(_) {},
    set selectedMediaIds(_) {},
    set attachmentsDomain(_) {},
    set errorTitle(_) {},
    set errorSubtitle(_) {},
    set selectedRecordIds(_) {},

    async fetchImmichRecords(offset) {
        if (!this.state.needle) {
            return { records: [], isMaxed: false };
        }
        this.state.isFetchingImmich = true;
        try {
            const { isMaxed, images } = await this.immich.getImages(this.state.needle, offset, this.NUMBER_OF_RECORDS_TO_DISPLAY, this.props.orientation);
            this.state.isFetchingImmich = false;
            this.state.immichError = false;
            const existingIds = new Set(this.state.immichRecords.map(r => r.id));
            const newImages = images.filter(record => {
                if (existingIds.has(record.id)) {
                    return false;
                }
                existingIds.add(record.id);
                return true;
            });
            const records = newImages.map(record => {
                return Object.assign({}, record, {
                    url: record.url,
                    mediaType: 'immichRecord',
                });
            });
            return { isMaxed, records };
        } catch (e) {
            this.state.isFetchingImmich = false;
            if (e === 'no_access') {
                this.state.useImmich = false;
            } else {
                this.state.immichError = e;
            }
            return { records: [], isMaxed: true };
        }
    },

    async loadMore(...args) {
        await super.loadMore(...args);
        return this.keepLastImmich.add(this.fetchImmichRecords(this.state.immichRecords.length)).then(({ records, isMaxed }) => {
            this.state.immichRecords.push(...records);
            this.state.isMaxed = isMaxed;
        });
    },

    async search(...args) {
        await super.search(...args);
        await this.searchImmich();
    },

    async searchImmich() {
        if (!this.state.needle) {
            this.state.immichError = false;
            this.state.immichRecords = [];
            this.state.isMaxed = false;
        }
        return this.keepLastImmich.add(this.fetchImmichRecords(0)).then(({ records, isMaxed }) => {
            this.state.immichRecords = records;
            this.state.isMaxed = isMaxed;
        });
    },

    async onClickRecord(media) {
        this.props.selectMedia({ ...media, mediaType: 'immichRecord', query: this.state.needle });
        if (!this.props.multiSelect) {
            await this.props.save();
        }
    },

    async submitCredentials(url, apiKey) {
        this.state.immichError = null;
        await rpc('/website_immich/save_config', { url, api_key: apiKey });
        await this.searchImmich();
    },
});
ImageSelector.components = {
    ...ImageSelector.components,
    ImmichError,
};

patch(MediaDialog.prototype, {
    setup() {
        super.setup();

        this.immichService = useService('immich');
    },

    async save() {
        const selectedImages = this.selectedMedia[TABS.IMAGES.id];
        if (selectedImages) {
            const immichRecords = selectedImages.filter(media => media.mediaType === 'immichRecord');
            if (immichRecords.length) {
                await this.immichService.uploadImmichRecords(immichRecords, { resModel: this.props.resModel, resId: this.props.resId }, (attachments) => {
                    this.selectedMedia[TABS.IMAGES.id] = this.selectedMedia[TABS.IMAGES.id].filter(media => media.mediaType !== 'immichRecord');
                    this.selectedMedia[TABS.IMAGES.id] = this.selectedMedia[TABS.IMAGES.id].concat(attachments.map(attachment => ({...attachment, mediaType: 'attachment'})));
                });
            }
        }
        return super.save(...arguments);
    },
});
