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
            let html = 
                `<div id="meeting" style="background-color: rgb(53, 53, 53); margin:1%; padding: 1%; width: 25%;">
                    <span style="display:flex; justify-content:center; color: white; font-weight: bolder; font-size: x-large; padding: 5%;">Hello!</span>
                    <div style="background-color: rgb(85, 85, 85); padding: 1%;">
                        <span style="color: white; font-size: larger; padding-left: 2%">Date:</span>
                    </div>
                    <div style="padding: 1%;">
                        <span style="color: white; font-size: larger; padding-left: 2%">Today!</span>
                    </div>
                    <div style="background-color: rgb(85, 85, 85); padding: 1%;">
                        <span style="color: white; font-size: larger; padding-left: 2%">Place:</span>
                    </div>
                    <div style="padding: 1%;">
                        <span style="color: white; font-size: larger; padding-left: 2%">Everywhere</span>
                    </div>
                    <div style="background-color: rgb(85, 85, 85); padding: 1%;">
                        <span style="color: white; font-size: larger; padding-left: 2%">Participants:</span>
                    </div>
                    <div style="padding: 1% 1% 1% 3%;">
                        <span style="color: white; font-size: larger;">- Name 1 <br> - Name 2 <br> - Name 3</span>
                    </div>
                </div>`
            //span 1 = Meeting name
            //span 2 & 3 = Meeting date
            //span 4 & 5 = Meeting place
            //span 6 & 7 = Meeting participants
            return this._super.apply(this, arguments).then(function () {
                const parent = $('#controller_content');
                parent.innerHTML = html;
                if (parent.length === 1) {
                    parent.append(html);
                }

            });
        }
    })
})

//TODO: render and style a div for the meeting info,
//separete the div to difrent sections (with divs or span)
//put in test data (text and stuf)
