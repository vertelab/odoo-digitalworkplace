console.log("Start");
odoo.define("calendar_voting.voting_site_style", function (require) {
    "use strict";

    var ajax = require('web.ajax')
    var publicWidget = require('web.public.widget')
    publicWidget.registry.calendarVoting = publicWidget.Widget.extend({
        selector: '#test_style',
        
        /**
         * @override
         */
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                const parent = $('#test_style');
                var div = document.createElement("div");
                div.id = "meeting_info";
                if (parent.length === 1) {
                    parent.append(div);
                }

        });
    }})
})
