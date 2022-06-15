console.log("Start");
odoo.define("calendar_voting.controller_voting", function (require) {
    "use strict";

    var ajax = require('web.ajax')
    var publicWidget = require('web.public.widget')
    publicWidget.registry.calendarVoting = publicWidget.Widget.extend({
        selector: '#controller_content',
        read_events: {
            'click .cell-voting-time': '_toggle_cell_on',
            'click .cell-voted-time': '_toggle_cell_off',
        },
        
        /**
         * @override
         */
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                const parent = $('#controller_content');
                console.log(parent.data("days-true"));
            });
        },

        _toggle_cell_on: function(e) {
            let button = $(e.target).click(function(){
            });
            button.removeClass("cell-voting-time");
            button.addClass("cell-voted-time");
        },

        _toggle_cell_off: function(e) {
            let button = $(e.target).click(function(){
            });
            button.removeClass("cell-voted-time");
            button.addClass("cell-voting-time");
        },
    })
})

