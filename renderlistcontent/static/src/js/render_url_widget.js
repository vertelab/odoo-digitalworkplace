odoo.define('renderlistcontent.renderer', function (require) {
    "use strict";

    /**
     * This file defines the Render List Content Widget for Many2Many and One2Many relations. 
     * If a URL is found within a given text, this widget will display the URL accordingly.
     * 
     * The URL must have spaces around it to be parsed out of a piece of text correctly, 
     * otherwise it will be ignored. 
     * URLs must start with "http://" or "https://" to be valid.
     * If the content is just a URL, then it will be parsed correctly.
     */

    const core = require('web.core');
    const registry = require('web.field_registry');
    const relational_fields = require('web.relational_fields');
    const FieldMany2ManyTags = relational_fields.FieldMany2ManyTags;

    const _t = core._t;

    const RenderListContent = FieldMany2ManyTags.extend({
        description: _t("Content"),
        tag_template: "RenderListContent",
        className: "o_field_renderlistcontent",
        supportedFieldTypes: ['one2many', 'many2many'],

        /**
         * @override
         * Make sure when you inherit this Widget to override this attribute
         * with column names of the model that is referenced. 
         * 
         * This field lets the widget know what fields to actually display
         * from the Many2Many relational model.
         */
        fieldsToFetch: {
            content: {type: 'text'},
        },

        /**this.contentToLoad.length
         * @private
         */
        _getRenderTagsContext: function () {
            return this.value ? _.pluck(this.value.data, 'data') : [];
        },

        /**
         * @override
         */
        _renderTags: function () {
            const parsed = this._parsedContent();
            const $this = this;
            this.$el.html(parsed).ready(function () {
                $this._loadWebContent();
            });
        },

        _loadWebContent: function () {
            if (!this.contentToLoad || !this.contentToLoad.length) return;
            for (let i = 0; i < this.contentToLoad.length; i++) {
                const c = this.contentToLoad[i];
                const e = document.getElementById(c);
                const url = e.getAttribute('data-url');
                if (!url) continue;
                this._grabURLdetails(url, (res) => {
                    e.innerHTML = `
                        <a href='${url}' target='_blank'>
                            <strong>${_t(res[0])}</strong>
                        </a>
                        <p>${_t(res[1])}</p>
                        <img src='${_t(res[2])}'/>
                    `;
                });
            }
        },

        /**
         * @private
         */
        _grabURLdetails: function (url, cb) {
            jQuery.ajax(url).done((res) => {
                const html = new DOMParser().parseFromString(res, 'text/html');
                const metas = html.head.querySelectorAll('meta[property]');
        
                const tmp = new URL(url);
                const props = ['Untitled', '', tmp.origin + '/favicon.ico'];
                for (let i = 0; i < metas.length; i++) {
                    const meta = metas[i];
        
                    const prop = meta.getAttribute('property');
        
                    if (prop.indexOf('title') > -1) {
                        props[0] = _t(meta.content);
                    } else if (prop.indexOf('description') > -1) {
                        props[1] = _t(meta.content);
                    } else if (prop.indexOf('image') > -1) {
                        if (meta.content.indexOf('http') === -1) {
                            meta.content = tmp.origin + meta.content
                        }

                        props[2] = meta.content;
                    }
                }
        
                cb(props);
            }).fail(() => {
                const tmp = new URL(url); 
                jQuery.ajax('/render' + tmp.origin.substring(tmp.protocol.length + 1)).then(function (res) {
                    const r = JSON.parse(res);

                    r.res[0] = _t(r.res[0]);
                    r.res[1] = _t(r.res[1]);

                    cb(r.res);
                }).catch(function () {
                    cb([_t('Error'), _t('404'), '/renderlistcontent/static/src/img/404PageNotFound.png']);
                })
            });
        },

        /**
         * @private
         */
        _checkExtension: function (string, uid) {
            if (!string) return '';
            const suffix = string.substring(string.lastIndexOf('.'));
            if (suffix.indexOf('.png') > -1 || suffix.indexOf('.jpg') > -1 || suffix.indexOf('.jpeg') > -1 || suffix.indexOf('.gif') > -1 || suffix.indexOf('.svg') > -1) {
                return `<img src="${string}"/>`;
            } else if (suffix.indexOf('.mp4') > -1 || suffix.indexOf('.webm') > -1 || suffix.indexOf('.ogg') > -1) {
                return `<video controls><source src="${string}"> This browser does not support video tag.</video>`;
            } else {
                if (!this.contentToLoad) this.contentToLoad = [];
                const id = 'loading-' + uid;
                this.contentToLoad.push(id);
                return `
                <div id="${id}" data-url="${string}" class="o_list_content_web_snippet">${_t('loading ...')}</div>
                `;
            }
        },

        /**
         * @private
         */
        _parseText: function (text, id) {
            if (!text) return '';
            const split = text.split('\n');
            return split.map((b) => {
                const g = b.split(' ').map((t) => {
                    const https = t.indexOf('https://');
                    const http = t.indexOf('http://');
    
                    let sub;
                    if (https > -1) {
                        sub = encodeURI(t.substring(https));
                    } else if (http > -1) {
                        sub = encodeURI(t.substring(http));
                    }
                    
                    if (sub) {
                        return this._checkExtension(sub, id);
                    } 
                    
                    if (!t) return '';
                    else return _t(this._toHTMLCode(t));
                }).join(' ');
                return `<div>${g}</div>`;
            }).join(' ');
        },

        /**
         * @private
         */
        _toHTMLCode: function (text) {
            if (!text) return '';
            let sign = text.indexOf('<');
            while (sign > -1) {
                text = text.substring(0, sign) + '&lt;' + text.substring(sign + 1);
                sign = text.indexOf('<');
            }

            sign = text.indexOf('>');
            while (sign > -1) {
                text = text.substring(0, sign) + '&gt;' + text.substring(sign + 1);
                sign = text.indexOf('>');
            }

            return text;
        },

        /** 
         * @private
         */
        _parsedContent: function () {
            return this._getRenderTagsContext().map((elm) => {
                let text = '';
                for (let f in this.fieldsToFetch) {
                    text += this._parseText(elm[f], elm.id) + ' ';
                }
                return text;
            }).join(' ');
        },
    });

    registry.add("render_list_content", RenderListContent);

});