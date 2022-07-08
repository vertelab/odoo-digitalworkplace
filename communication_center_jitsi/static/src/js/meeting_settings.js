odoo.define("communication_center_jitsi.metting_settings.js", function (require) {
    "use strict";

    var ajax = require('web.ajax')
    var publicWidget = require('web.public.widget')
    publicWidget.registry.jitsiMeetSettingsButtons = publicWidget.Widget.extend({
        selector: '#jitsi_meeting_placeholder',
        read_events: {
            'click .jitsi_button_lobby': '_toggle_lobby',
            'click .jitsi_button_rec': '_toggle_record',
            'click .jitsi_button_room': '_toggle_room',
            'click .jitsi_button_fullscreen': '_toggle_screen',
        },

        check_lobby: function (lobby_with_knocking, lobby_with_name) {
            if (lobby_with_knocking && lobby_with_name) {
                return true
            } else if (lobby_with_knocking || lobby_with_name) {
                return true
            } else {
                return false
            }
        },
        //--------------------------------------------------------------------------
        // Lifetime Methods
        //--------------------------------------------------------------------------

        /**
        * @override
        */
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                const parent = $('#jitsi_meeting_placeholder');
                var div = document.createElement("div");
                div.id = "center_meeting";
                if (parent.length === 1) {
                    parent.append(div);
                }
                const domain = parent.data("jitsi");
                const jwt_token = parent.data("jwt");
                const lobby_with_knocking = parent.data('lobby_with_knocking');
                const lobby_with_name = parent.data('lobby_with_name');

                //Check if there is a lobby.
                self.unicId = parent.data("link_suffix");
                self.rec_on_start = parent.data('start_recording');
                self.no_recording = parent.data('no_recording');
                self.Lobby_on = self.check_lobby(lobby_with_knocking, lobby_with_name);
                self.Toggle_recording = false;

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

                if (self.no_recording) {
                    toolbarButtons.splice(toolbarButtons.indexOf('livestreaming'), 1);
                    toolbarButtons.splice(toolbarButtons.indexOf('recording'), 1);
                };

                let roomSubject = parent.data("room_subject");
                if (parent.data("room_subject") == undefined){
                    roomSubject = parent.data("meeting_subject")}

                const options = {
                    roomName: self.unicId,
                    width: 1500,
                    height: 700,
                    parentNode: div,
                    jwt: jwt_token,
                    // onload: function () {
                    //     if (self.rec_on_start) {
                    //         self.api.executeCommand('startRecording', {
                    //             mode: 'file'
                    //         })
                    //         self.Toggle_recording = true
                    //     };
                    // },
                    configOverwrite:
                    {
                        requireDisplayName: self.Lobby_on,
                        prejoinPageEnabled: self.Lobby_on,
                        startWithAudioMuted: parent.data("microphone_off") == "True",
                        startWithVideoMuted: parent.data("webcam_off") == "True",
                        toolbarButtons: toolbarButtons,
                    },
                };

                self.api = new JitsiMeetExternalAPI(domain, options);
                
                self.api.executeCommand('subject', roomSubject);


                self._render_buttons(self.api, self.rec_on_start);

                // Removes the lingering jwt token from the dom tree.
                if (parent[0].attributes['data-jwt']) {
                    parent[0].removeAttribute('data-jwt')
                }

                console.log("DONEEEEEE")
            });
        },
        //--------------------------------------------------------------------------
        // Private Methods
        //--------------------------------------------------------------------------
        _render_buttons: function (api, rec_on_start) {
            let menu_html = `<div class='btn_holder' style='height:${this.$el.height()}px; width:auto; display:flex;'>   
                                <a id="lobby_btn" class='btn ${this.Lobby_on ? 'btn-on' : 'btn-off'} jitsi_button_lobby'>
                                ${this.Lobby_on ? '<i class="fa fa-lock" />' : '<i class="fa fa-unlock" />'}</a>
                                <a class='btn btn-room-react jitsi_button_room'>
                                <i class="fa fa-users" />
                                </a>
                                <a id="screen_btn" class='btn ${this.Lobby_on ? 'btn-on' : 'btn-off'} 
                                 jitsi_button_fullscreen'>
                                 <i class="fa fa-expand" /> </a>
                                </div>`
                                // ${self.menu_for_all}
            // let menu_for_all = `<a id="screen_btn" class='btn ${this.Lobby_on ? 'btn-on' : 'btn-off'} 
            //                     jitsi_button_fullscreen'>
            //                     <i class="fa fa-expand" /> </a>`
                                //${this._render_recording(rec_on_start)}   
                                
            api.addEventListener('participantRoleChanged', function (event) {
                console.log("participantRoleChanged", event);
                if (event.role === 'moderator') {
                    api.executeCommand('toggleLobby', true)
                    this.Lobby_on = true;
                    if ($('.btn_holder').length <= 0) {
                        $('#center_meeting').append(menu_html)
                    }
                }
                //else vass menu_for_all, det är knappen för helskärm, vet inte om koden jag skrev funkar, det är i test
            })
        },
        _toggle_server_lobby: function (client_link_suffix, client_lobby_status) {
            let uri = `/video_meeting/${client_link_suffix}/toggle_lobby`
            let toggleMenu = ajax.jsonRpc(uri, 'call', {
                link_suffix: client_link_suffix,
                lobby_status: client_lobby_status
            }).then(console.log(`Server Lobby Status: ${client_lobby_status}`))
        },

        // _render_recording: function (rec_on_start) {
        //     if (this.no_recording) {
        //         return ""
        //     } else if (rec_on_start) {
        //         return "   <a id='rec_btn' class='btn btn-primary jitsi_button_rec'>Stop Recording!</a>"
        //     } else {
        //         return "   <a id='rec_btn' class='btn btn-success jitsi_button_rec'>Start Recording!</a>"
        //     }
        // },

        _toggle_lobby: function (e) {
            console.log("TOGGLE LOBBY");
            let button = $(e.target)
            let the_button = document.getElementById("lobby_btn");
            console.log(the_button)
            if (this.Lobby_on) {
                this.api.executeCommand('toggleLobby', false)
                this.Lobby_on = false
                this._toggle_server_lobby(this.unicId, this.Lobby_on)

                the_button.classList.replace("btn-on", "btn-off");
                the_button.innerHTML = '<i class="fa fa-unlock" />';
                console.log(the_button)
            } else {
                this.api.executeCommand('toggleLobby', true)
                this.Lobby_on = true
                this._toggle_server_lobby(this.unicId, this.Lobby_on)

                the_button.classList.replace("btn-off", "btn-on");
                the_button.innerHTML = '<i class="fa fa-lock" />';
                console.log(the_button)
            }
        },

        _toggle_record: function (e) {
            let button = $(e.target)
            let the_button2 = document.getElementById("rec_btn");
            console.log(button)
            console.log(e)
          
            if (!this.Toggle_recording) {
                this.Toggle_recording = true;
                this.api.executeCommand('startRecording', {
                    mode: 'file'
                })
                the_button2.classList.replace("btn-success", "btn-primary");
                the_button2.innerHTML = "<p>New Text</p>";
            }
            else if (this.Toggle_recording) {
                this.Toggle_recording = false;
                this.api.executeCommand('stopRecording', {
                    mode: 'file'
                })
                the_button2.classList.replace("btn-primary", "btn-success");
                the_button2.innerHTML = "<i class='fa fa-users'></i>";
            }
        },

        _toggle_room: function () {
            console.log(this.api.getParticipantsInfo())
            this.api.executeCommand('addBreakoutRoom', 'room')
        },
        _toggle_screen: function () {
            document.querySelector("#jitsiConferenceFrame0").requestFullscreen();
        }

    })
});

