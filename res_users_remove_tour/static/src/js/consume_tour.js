odoo.define('web.DebugManager.Backend.Extended', function (require) {
    "use strict";

    var core = require("web.core");
    var Dialog = require("web.Dialog");
    var local_storage = require('web.local_storage');
    var tour = require('web_tour.tour');
    var utils = require('web_tour.utils');
    var DebugManagerOdoo = require('web.DebugManager.Backend');
    


    DebugManagerOdoo.extend({
        events: _.extend({
            "click .js_class": "remove_tour",
        }),
        remove_tour: function () {
            console.log('Button Clicked')
        },
    })
})