console.log("Start");
odoo.define("calendar_voting.controller_voting", function (require) {
    "use strict";

    var ajax = require('web.ajax')
    var publicWidget = require('web.public.widget')
    publicWidget.registry.calendarVoting = publicWidget.Widget.extend({
        selector: '#controller_content',
        
        /**
         * @override
         */
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                const parent = $('#controller_content');
            });
        }
    })
})

