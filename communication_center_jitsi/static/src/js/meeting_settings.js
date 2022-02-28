console.log("start");
odoo.define("communication_center_jitsi.metting_settings.js", function (require) {
    "use strict";

    console.log("after start");
    const rpc = require("web.rpc"); //maby create a funktion insted off APIsettings or add .this

    //console.log(rpc);
    /*const APIsettings = rpc.query({
        model: "ir.config_parameter",
        method: "get_param",
        args: ["communication_center_jitsi"],
    });*/
    console.log("sup")

    $('document').ready(function (event) {  //THISWORKS
        console.log("going");
        
        var div = document.createElement("div");
        div.id="center_meeting";
        const domain = $("#jitsi_meeting_placeholder").data("jitsi");
        const options = {
            roomName: $("#jitsi_meeting_placeholder").data("room_name"),
            width: 1500,
            height: 700,
            parentNode: div,
        };
        console.log(options.roomName)
        console.log(domain)

        
        rpc.query ({
            route: '/controllers/jitsi_controller.py',
            params: {'options': options},
        });
        console.log("WHT UP",rpc);
        /*options.roomName = options.Class.extend({
            _test_function: function() {
                console.log("anything");
            },
            
            init: function(){
                const _super = this._super.bind(this);
                console.log("somthing");
                return _super (...arguments);
            },

            testStart: async function () {
                    const _super = this._super.bind(this);
    
                    var data = await this.rpc ({
                        model:'calendar.event', 
                        method:'room_name',
                    });
                    console.log("Exit");
            return _super(...arguments);*/
        
            var api = new JitsiMeetExternalAPI(domain, options);
            
            api.addEventListener('participantRoleChanged', function (event) {
                if (event.role === 'moderator') {
                    api.executeCommand('toggleLobby', true);
                }
            })
            
            var perent = $('#jitsi_meeting_placeholder'); //Dont know id or think to poin to withch perent ot is?
            if (perent.length === 1)
            perent.append(div);
    });


    /*options.registry.video_meeting_chekbox = options.Class.extend({
        _test_function: function() {
            console.log("funktion before async");
        },
        
        StartPls: async function () {
            console.log("wait for it")
            const _super = this_super.bind(this);
            
            console.log("go!");
            var data = await this.rpc({
                model: 'calendar.event',  //namnet på filen (py)
                method: 'button_test', //namnet på funktionen i filen
            });
            
            console.log(data);
            //vad ska hända
            return alert("SUP!!!");
        },
    });*/

});
console.log("end");
