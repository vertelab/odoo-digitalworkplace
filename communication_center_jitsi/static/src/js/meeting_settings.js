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

        let Lobby_onoff = "Off";

        const domain = parent.data("jitsi");

        let roomName= parent.data("room_name")
        console.log(roomName);

    const options = {
        roomName: roomName,
        width: 1500,
            height: 700,
            parentNode: div,
            configOverwrite: 
            { 
                requireDisplayName: parent.data("lobby_with_name") == "True",
                prejoinPageEnabled: parent.data("lobby_with_name") == "True",
                startWithAudioMuted: parent.data("microphone_off") == "True", 
                startWithVideoMuted: parent.data("webcam_off") == "True",
            },
            
        };

            let api = new JitsiMeetExternalAPI(domain, options);
            
            if (parent.data("lobby_with_knocking") == "True"){
            api.addEventListener('participantRoleChanged', function (event) {
                console.log("event", event);
                if (event.role === 'moderator') {
                    api.executeCommand('toggleLobby', true)
                    Lobby_onoff = "On";
                }
            })};

            var jitsi_button_lobby = $(".jitsi_button_lobby");
            jitsi_button_lobby.on("click", function (){
                console.log()
                if (Lobby_onoff == "On") {
                    api.executeCommand('toggleLobby', false)
                    Lobby_onoff = "Off"
                    alert("Lobby off")
                    jitsi_button_lobby.while (1); {
                        jitsi_button_lobby.innerText("Lobby on!")
                    };
                } else if (Lobby_onoff == "Off") {
                    api.executeCommand('toggleLobby', true)
                    Lobby_onoff = "On"
                    alert("Lobby on")
                    jitsi_button_lobby.while (); {
                        jitsi_button_lobby.innerText("Lobby off!")
                    };
                }
            });

            var jitsi_button = $(".jitsi_button");
            jitsi_button.innerText="Hello?"
            jitsi_button.on("click", function (){
                api.executeCommand('toggleRaiseHand');
                console.log('api', api);
            });

            if (parent.data("start_recording") == "True"){
                console.log("REC");
                api.executeCommand('startRecording')
            };
            console.log(parent.data("start_recording"))
            console.log("HEEYYYY")

            var jitsi_button = $(".jitsi_button_recoff");
            jitsi_button.on("click", function (){
                console.log("REC OFF");
                api.executeCommand('stopRecording', true)
            });

        console.log("event", event);
    });
});

