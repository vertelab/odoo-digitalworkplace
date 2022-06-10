console.log("Start");
odoo.define("calendar_voting.voting_site_style", function (require) {
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
            //span 1 = Meeting name
            //span 2 & 3 = Meeting date
            //span 4 & 5 = Meeting place
            //span 6 & 7 = Meeting participants
            return this._super.apply(this, arguments).then(function () {
                const parent = $('#controller_content');
                // parent.innerHTML = html;
                // if (parent.length === 1) {
                //     parent.append(html);
                // }

            });
        }
    })
})

//TODO: render and style a div for the meeting info,
//separete the div to difrent sections (with divs or span)
//put in test data (text and stuf)
