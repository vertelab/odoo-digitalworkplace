import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { AUTOCLOSE_DELAY } from "@html_editor/main/media/media_dialog/upload_progress_toast/upload_service";

const immichLogger = {
    debug: (...args) => console.debug("[Immich]", ...args),
    error: (...args) => console.error("[Immich]", ...args),
};

export const immichService = {
    dependencies: ["upload"],
    async start(env, { upload }) {
        immichLogger.debug("Immich service started");
        const _cache = {};
        return {
            async uploadImmichRecords(records, { resModel, resId }, onUploaded) {
                immichLogger.debug("Uploading Immich records:", records.length, records[0]?.query);
                upload.incrementId();
                const file = upload.addFile({
                    id: upload.fileId,
                    name:
                        records.length > 1
                            ? _t("Uploading %(count)s '%(query)s' images.", {
                                  count: records.length,
                                  query: records[0].query,
                              })
                            : _t("Uploading '%s' image.", records[0].query),
                });

                try {
                    const assets = {};
                    for (const record of records) {
                        assets[record.id] = {
                            original_url: record.original_url,
                            description: record.original_filename,
                        };
                    }

                    const xhr = new XMLHttpRequest();
                    xhr.upload.addEventListener("progress", (ev) => {
                        const rpcComplete = (ev.loaded / ev.total) * 100;
                        file.progress = rpcComplete;
                    });
                    xhr.upload.addEventListener("load", function () {
                        file.progress = 100;
                    });
                    const attachments = await rpc(
                        "/website_immich/attachment/add",
                        {
                            res_id: resId,
                            res_model: resModel,
                            assets: assets,
                            query: records[0].query,
                        },
                        { xhr }
                    );

                    if (attachments.error) {
                        file.hasError = true;
                        file.errorMessage = attachments.error;
                    } else {
                        file.uploaded = true;
                        await onUploaded(attachments);
                    }
                    setTimeout(() => upload.deleteFile(file.id), AUTOCLOSE_DELAY);
                } catch (error) {
                    file.hasError = true;
                    setTimeout(() => upload.deleteFile(file.id), AUTOCLOSE_DELAY);
                    throw error;
                }
            },

            async getImages(query, offset = 0, pageSize = 30, orientation) {
                immichLogger.debug("getImages called:", { query, offset, pageSize });
                const from = offset;
                const to = offset + pageSize;
                let cachedData = _cache[query];

                if (
                    cachedData &&
                    (cachedData.images.length >= to ||
                        (cachedData.totalImages !== 0 && cachedData.totalImages < to))
                ) {
                    return {
                        images: cachedData.images.slice(from, to),
                        isMaxed: to > cachedData.totalImages,
                    };
                }
                cachedData = await this._fetchImages(query, orientation);
                return {
                    images: cachedData.images.slice(from, to),
                    isMaxed: to > cachedData.totalImages,
                };
            },

            invalidateCache(query) {
                if (query) {
                    delete _cache[query];
                    immichLogger.debug("Cache invalidated for query:", query);
                } else {
                    Object.keys(_cache).forEach(k => delete _cache[k]);
                    immichLogger.debug("Full cache invalidated");
                }
            },

            async _fetchImages(query, orientation) {
                immichLogger.debug("_fetchImages:", { query, page: _cache[query]?.page ? _cache[query].page + 1 : 1 });
                if (!_cache[query]) {
                    _cache[query] = {
                        images: [],
                        page: 0,
                        totalImages: 0,
                    };
                }
                const cachedData = _cache[query];
                const payload = {
                    query: query,
                    page: cachedData.page + 1,
                    size: 30,
                };
                const result = await rpc("/website_immich/fetch_images", payload);
                if (result.error) {
                    immichLogger.error("fetch_images error:", result.error);
                    return Promise.reject(result.error);
                }
                immichLogger.debug("fetch_images result:", { total: result.total, count: result.images?.length });
                cachedData.page++;
                cachedData.images.push(...result.images);
                cachedData.totalImages = result.total;
                return cachedData;
            },
        };
    },
};

registry.category("services").add("immich", immichService);
