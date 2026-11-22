odoo.define('discuss_show_members/static/src/components/discuss_sidebar_item/discuss_sidebar_item.js', function (require) {
    'use strict';

    const { isEventHandled } = require('mail/static/src/utils/utils.js');

    const components = {
        DiscussSidebarItem: require('mail/static/src/components/discuss_sidebar_item/discuss_sidebar_item.js'),
    };

    const { patch } = require('web.utils');

    patch(components.DiscussSidebarItem, 'discuss_show_members/static/src/components/discuss/discuss.js', {

        _onClick(ev) {
            $('[data-toggle="popover"]').popover('hide')

            $('[data-toggle="popover"]').popover({
                placement: 'top',
                trigger: 'click'
            }).attr(
                'data-content', this.thread.members.map(member => '<div>' + member.name + '</div>')
            );
            if (isEventHandled(ev, 'EditableText.click')) {
                return;
            }
            this.thread.open();
        }
    });
});