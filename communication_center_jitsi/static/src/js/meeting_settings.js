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
        const domain = 'meet.vertel.se'; //TODO: fetch url from the feld thats in setings in odoo   <field name="jitsi_url"/> in res_config
        const options = {
            roomName: 'JitsiMeetAPIExample4567', //make so the user can set roomName  <field name="room_name"/> in res_config
            width: 1500,
            height: 700,
            parentNode: div,
        };
        var api = new JitsiMeetExternalAPI(domain, options);

        console.log("maby?");
        api.addEventListener('participantRoleChanged', function (event) {
            if (event.role === 'moderator') {
                api.executeCommand('toggleLobby', true);
            }
        })

        console.log("Hi!!")
        console.log(api)
        console.log(perent)
        console.log(div)
        var perent = $('#jitsi_meeting_placeholder'); //Dont know id or think to poin to withch perent ot is?
        if (perent.length === 1)
        perent.append(div);
        console.log(perent);
        console.log(perent.length);
    });

    options.registry.video_meeting_chekbox = options.Class.extend({
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
    });

});
console.log("end");
