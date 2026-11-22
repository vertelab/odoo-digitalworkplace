console.log("Start");
odoo.define("calendar_voting.controller_voting", function (require) {
    "use strict";

    var rpc = require('web.rpc');
    var ajax = require('web.ajax')
    var publicWidget = require('web.public.widget')
    publicWidget.registry.calendarVoting = publicWidget.Widget.extend({
        selector: '#controller_content',
        read_events: {
            'click .cell-voting-time': '_toggle_cell_on',
            'click .cell-voted-time': '_toggle_cell_off',
            'click .cell-voting': '_voting_off',
        },
        
        /**
         * @override
         */
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                const parent = $('#controller_content');
            });
        },
        
        _toggle_cell_on: function(e) {
            let button = $(e.target).click(function(){
                console.log(button);
            });
            const voting_stop = document.getElementById("voting-button")
            if (voting_stop.classList.contains("cell-voting")){
                button.removeClass("cell-voting-time");
                button.addClass("cell-voted-time");
            }},
            
        _toggle_cell_off: function(e) {
            let button = $(e.target).click(function(){
                console.log(button);
            });
            const voting_stop = document.getElementById("voting-button")
            if (voting_stop.classList.contains("cell-voting")){
                button.removeClass("cell-voted-time");
                button.addClass("cell-voting-time");
            }},

        _voting_off: function (e) {
            let voting = $(e.target).click(function(){
                console.log(voting)
            })
            voting.removeClass("cell-voting");
            voting.addClass("cell-voted");

            this._results(e)
        },

        _results: function (e) {
            let voting_id = $(e.target).data("id");
            let cell_one = document.getElementById("cell-1");
            let cell_tow = document.getElementById("cell-2");
            let cell_three = document.getElementById("cell-3");
            let cell_four = document.getElementById("cell-4");
            let cell_five = document.getElementById("cell-5");

            const dict = {
                monday : cell_one.classList.contains("cell-voted-time"),
                tuesday : cell_tow.classList.contains("cell-voted-time"),
                wednesday : cell_three.classList.contains("cell-voted-time"),
                thursday : cell_four.classList.contains("cell-voted-time"),
                friday : cell_five.classList.contains("cell-voted-time"),
            }
            console.log(dict)
            console.log(voting_id)

            rpc.query({
                model: "calendar.voting",
                method: "write",
                args:  [voting_id, dict],
            });

        }
    })
})

