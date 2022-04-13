odoo.define("communication_center_jitsi.metting_settings.js", function (require) {
    "use strict";

    const rpc = require("web.rpc");


    $('document').ready(function (event) {
        
        var div = document.createElement("div");
        div.id="center_meeting";
        var parent = $('#jitsi_meeting_placeholder');
        if (parent.length === 1){
            parent.append(div);
            console.log("parent.append(div);");
        }

        let Lobby_on = false;
        let Rec_on = false;

        const domain = parent.data("jitsi");

        let unicId = parent.data("link_suffix");
        let toolbarButtons = [
            'camera',
            'chat',
            'closedcaptions',
            'desktop',
            'download',
            'embedmeeting',
            'etherpad',
            'feedback',
            'filmstrip',
            'fullscreen',
            'hangup',
            'help',
            'highlight',
            'livestreaming',
            'recording',
            'invite',
            'linktosalesforce',
            'microphone',
            'mute-everyone',
            'mute-video-everyone',
            'participants-pane',
            'profile',
            'raisehand',
            'security',
            'select-background',
            'settings',
            'shareaudio',
            'sharedvideo',
            'shortcuts',
            'stats',
            'tileview',
            'toggle-camera',
            'videoquality',
            '__end'
        ];
        
        if (parent.data("no_recording") == "True") {
            toolbarButtons.splice(toolbarButtons.indexOf('livestreaming'),1);
            toolbarButtons.splice(toolbarButtons.indexOf('recording'),1);
        };
        console.log(toolbarButtons);

        const options = {
            roomName: unicId,
            width: 1500,
            height: 700,
            parentNode: div,
            configOverwrite: 
            { 
                requireDisplayName: parent.data("lobby_with_name") == "True",
                prejoinPageEnabled: parent.data("lobby_with_name") == "True",
                startWithAudioMuted: parent.data("microphone_off") == "True", 
                startWithVideoMuted: parent.data("webcam_off") == "True",
                toolbarButtons: toolbarButtons,
            },
            
        };

            let api = new JitsiMeetExternalAPI(domain, options);

            let roomSubject = " "
            if (parent.data("room_subject") == undefined){
                roomSubject = "happy"}
            else if (parent.data("room_subject") !== ""){
                roomSubject = parent.data("room_subject")};

            api.executeCommand('subject', roomSubject);
            
            var jitsi_button_lobby = $(".jitsi_button_lobby");
            if (parent.data("lobby_with_knocking") == "True"){
                jitsi_button_lobby.each (function(){
                    this.innerText="Lobby on!";
                    $(this).addClass('btn-success');
                    $(this).removeClass('btn-primary');
                });
                api.addEventListener('participantRoleChanged', function (event) {
                    console.log("participantRoleChanged", event);
                    if (event.role === 'moderator') {
                        api.executeCommand('toggleLobby', true)
                        Lobby_on = true;
                    }
                })};

            jitsi_button_lobby.on("click", function (){
                console.log()
                if (Lobby_on === true) {
                    api.executeCommand('toggleLobby', false)
                    Lobby_on = false
                    jitsi_button_lobby.each (function (){
                        this.innerText ="Lobby off!";
                        $(this).addClass('btn-primary');
                        $(this).removeClass('btn-success');
                    });
                } else if (Lobby_on === false) {
                    api.executeCommand('toggleLobby', true)
                    Lobby_on = true
                    jitsi_button_lobby.each (function(){
                        this.innerText="Lobby on!";
                        $(this).addClass('btn-success');
                        $(this).removeClass('btn-primary');
                    });
                }
            });

            var jitsi_button = $(".jitsi_button");
            jitsi_button.innerText="Hello?"
            jitsi_button.on("click", function (){
                api.executeCommand('toggleRaiseHand');
                console.log('api', api);
            });

            var jitsi_button_rec = $(".jitsi_button_rec");
            if (parent.data("start_recording") == "True"){
                console.log("REC");
                api.executeCommand('startRecording',{
                    mode: 'file'
                })
                jitsi_button_rec.each (function(){
                    this.innerText="Stop Recording!";
                    $(this).addClass('btn-primary');
                    $(this).removeClass('btn-success');
                    Rec_on = true;
            })
            };

            jitsi_button_rec.on("click", function (){
                console.log("REC");
                if (Rec_on === false){
                    Rec_on = true;
                    api.executeCommand('startRecording',{
                        mode: 'file'})
                        jitsi_button_rec.each (function(){
                            this.innerText="Stop Recording!";
                            $(this).addClass('btn-primary');
                            $(this).removeClass('btn-success');
                    })
                }
                else if (Rec_on === true){
                    Rec_on = false;
                    api.executeCommand('stopRecording', true)
                    jitsi_button_rec.each (function(){
                        this.innerText="Start Recording!";
                        $(this).addClass('btn-success');
                        $(this).removeClass('btn-primary');
                })
                }
                else if (parent.data("no_recording") == "True"){
                    jitsi_button_rec.each (function(){
                        $(this).addClass(disabled);
                })
            }
            });

            var jitsi_button_room = $(".jitsi_button_room");
            jitsi_button_room.on("click", function(){
                api.executeCommand('addBreakoutRoom',
                    name,)
            });
        console.log("event", event);
    });
});

