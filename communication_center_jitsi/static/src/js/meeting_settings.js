odoo.define("communication_center_jitsi.metting_settings.js", function (require) {
    "use strict";

    const rpc = require("web.rpc");


    $('document').ready(function (event) {
        
        var div = document.createElement("div");
        div.id="center_meeting";
        var parent = $('#jitsi_meeting_placeholder');
        if (parent.length === 1){
            parent.append(div);
        }
        const domain = parent.data("jitsi");

        let roomName= parent.data("room_name") //$("#jitsi_meeting_placeholder").data("link_suffix")
        console.log(roomName);

        /*
        roomName += "config.startWithAudioMuted=true&"
        console.log(roomName)
    };
    if ($("#jitsi_meeting_placeholder").data("webcam_off") == "True") {
        roomName += "config.startWithVideoMuted=true&"
        console.log(roomName)
    };*/
    
    /*event = {
        toggleLobby: 'toggle-lobby',
        displayName: 'display-name'
    };
    const commands ={
        toggleLobby: 'toggle-lobby',
        displayName: 'display-name'
    };*/
    
    // console.log(roomName);
    const options = {
        roomName: roomName,
        width: 1500,
            height: 700,
            parentNode: div,
            configOverwrite: { startWithAudioMuted: parent.data("microphone_off") == "True" },
            //<toggleLobby: 'toggleLobby'
        };
        console.log(options.configOverwrite.startWithAudioMuted)

        /*rpc.query ({
            route: '/controllers/jitsi_controller.py',
            params: {'options': options},
        });*/

            let api = new JitsiMeetExternalAPI(domain, options);


            // api.executeCommand('displayName', 'New Nickname');

            // api.executeCommand('toggleLobby', true);
            
            api.addEventListener('participantRoleChanged', function (event) {
                console.log("event", event);
                if (event.role === 'moderator') {
                    api.executeCommand('toggleLobby', true)
                }
            });

            /*api.addEventListener('videoConferenceStart',() => {
                api.executeCommand('startShareVideo', "https://www.youtube.com/watch?v=JUAYFoRWU5g")
            });*/
            // var parent = $('#jitsi_meeting_placeholder');
            // if (parent.length === 1){
            //     parent.append(div);
            // }
            var jitsi_button = $(".jitsi_button");
            jitsi_button.innerText="Hello?"
            jitsi_button.on("click", function (){
                api.executeCommand('toggleRaiseHand');
                //console.log(api.executeCommand('startShareVideo', "https://www.youtube.com/watch?v=JUAYFoRWU5g"));
                console.log('api', api);
            });
            console.log("event", event);

    });
});

