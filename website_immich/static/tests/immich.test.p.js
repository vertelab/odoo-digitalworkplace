import { setupEditor } from "@html_editor/../tests/_helpers/editor";
import { insertText } from "@html_editor/../tests/_helpers/user_actions";
import { expectElementCount } from "@html_editor/../tests/_helpers/ui_expectations";
import { expect, test } from "@odoo/hoot";
import { animationFrame, click, Deferred, press, waitFor } from "@odoo/hoot-dom";
import { contains, makeMockEnv, onRpc } from "@web/../tests/web_test_helpers";

test("Immich is inserted in the Media Dialog", async () => {
    const imageRecord = {
        id: 1,
        name: "logo",
        mimetype: "image/png",
        image_src: "/web/static/img/logo2.png",
        access_token: false,
        public: true,
    };
    onRpc("ir.attachment", "search_read", () => [imageRecord]);
    const fetchDef = new Deferred();
    onRpc("/website_immich/fetch_images", () => {
        expect.step("fetch_images");
        fetchDef.resolve();
        return {
            total: 1,
            images: [
                {
                    id: "immich-asset-123",
                    type: "IMAGE",
                    url: "/web/static/img/logo2.png",
                    original_url: "/web/static/img/logo2.png",
                    original_filename: "photo.jpg",
                    thumbhash: "",
                    exif_info: {
                        width: 800,
                        height: 600,
                    },
                },
            ],
        };
    });
    onRpc("/website_immich/attachment/add", (args) => [
        { ...imageRecord, description: "immich_image" },
    ]);
    const env = await makeMockEnv();
    const { editor } = await setupEditor(`<p>[]</p>`, { env });
    await expectElementCount(".o-we-powerbox", 0);
    await insertText(editor, "/image");
    await animationFrame();
    await expectElementCount(".o-we-powerbox", 1);
    await click(".o-we-command");
    await animationFrame();
    expect(".o_select_media_dialog").toHaveCount(1);
    contains("input.o_we_search").edit("cat");
    await fetchDef;
    expect.verifySteps(["fetch_images"]);
    await waitFor("img[title='photo.jpg']");
    await click("img[title='photo.jpg']");
    await waitFor(".o-wysiwyg img[alt='immich_image']");
    expect(".o-wysiwyg img[alt='immich_image']").toHaveCount(1);
});

test("Immich error is displayed when there is no config", async () => {
    const imageRecord = {
        id: 1,
        name: "logo",
        mimetype: "image/png",
        image_src: "/web/static/img/logo2.png",
        access_token: false,
        public: true,
    };
    onRpc("ir.attachment", "search_read", () => [imageRecord]);
    const fetchDef = new Deferred();
    onRpc("/website_immich/fetch_images", () => {
        fetchDef.resolve();
        return {
            error: "config_not_found",
        };
    });
    const env = await makeMockEnv();
    const { editor } = await setupEditor(`<p>[]</p>`, { env });
    await expectElementCount(".o-we-powerbox", 0);
    await insertText(editor, "/image");
    await animationFrame();
    await expectElementCount(".o-we-powerbox", 1);
    await click(".o-we-command");
    await animationFrame();
    expect(".o_select_media_dialog").toHaveCount(1);
    contains("input.o_we_search").edit("cat");
    await fetchDef;
    await waitFor(".immich_error");
    expect(".immich_error").toHaveCount(1);
});

test("Immich connection error is displayed", async () => {
    const imageRecord = {
        id: 1,
        name: "logo",
        mimetype: "image/png",
        image_src: "/web/static/img/logo2.png",
        access_token: false,
        public: true,
    };
    onRpc("ir.attachment", "search_read", () => [imageRecord]);
    const fetchDef = new Deferred();
    onRpc("/website_immich/fetch_images", () => {
        fetchDef.resolve();
        return {
            error: "connection_error",
        };
    });
    const env = await makeMockEnv();
    const { editor } = await setupEditor(`<p>[]</p>`, { env });
    await expectElementCount(".o-we-powerbox", 0);
    await insertText(editor, "/image");
    await animationFrame();
    await expectElementCount(".o-we-powerbox", 1);
    await click(".o-we-command");
    await animationFrame();
    expect(".o_select_media_dialog").toHaveCount(1);
    contains("input.o_we_search").edit("cat");
    await fetchDef;
    await waitFor(".immich_error");
    expect(".immich_error").toHaveCount(1);
});

test("Document tab does not crash with FileSelector extension", async () => {
    onRpc("ir.attachment", "search_read", () => [
        {
            id: 1,
            name: "logo",
            mimetype: "image/png",
            image_src: "/web/static/img/logo2.png",
            access_token: false,
            public: true,
        },
    ]);
    const env = await makeMockEnv();
    const { editor } = await setupEditor("<p>a[]</p>", { env });
    await insertText(editor, "/image");
    await animationFrame();
    await press("enter");
    await animationFrame();
    await click("li:nth-child(2) > a.nav-link");
    expect(".o_existing_attachment_cell").toHaveCount(1);
});
