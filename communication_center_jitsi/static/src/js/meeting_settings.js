odoo.define("communication_center_jitsi.metting_settings.js", function (require) {
    "use strict";

    const rpc = require("web.rpc");


    $('document').ready(function (event) {
        
        var div = document.createElement("div");
        div.id="center_meeting";
        const domain = $("#jitsi_meeting_placeholder").data("jitsi");
        const options = {
            roomName:  $("#jitsi_meeting_placeholder").data("link_suffix")+"/"+$("#jitsi_meeting_placeholder").data("room_name")+"#",
            width: 1500,
            height: 700,
            parentNode: div,
        };

        rpc.query ({
            route: '/controllers/jitsi_controller.py',
            params: {'options': options},
        });

            var api = new JitsiMeetExternalAPI(domain, options);
            api.executeCommand('toggleLobby', true);
            
            api.addEventListener('participantRoleChanged', function (event) {
                console.log("event", event);
                if (event.role === 'moderator') {
                    api.executeCommand('toggleLobby', true)
                }
            })
            
            var perent = $('#jitsi_meeting_placeholder');
            if (perent.length === 1)
            perent.append(div);
            console.log('api', api);

            api.executeCommand('displayName', 'New Nickname');

            $(".jitsi_button").on("click", function (){
                api.executeCommands({toggleLobby: [false]})
            });
    });
});

