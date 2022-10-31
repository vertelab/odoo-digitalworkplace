odoo.define("communication_center_jitsi.metting_settings.js", function(require) {
    "use strict";

    var ajax = require('web.ajax')
    var publicWidget = require('web.public.widget')
    let name_lobby_on_off;
    publicWidget.registry.jitsiMeetSettingsButtons = publicWidget.Widget.extend({
        selector: '#jitsi_meeting_placeholder',
        read_events: {
            'click .jitsi_button_knocking_lobby': '_toggle_knocking_lobby',
            'click .jitsi_button_name_lobby': '_toggle_name_lobby',
            'click .jitsi_button_rec': '_toggle_record',
            'click .jitsi_button_room': '_toggle_room',
            'click .jitsi_button_fullscreen': '_toggle_screen',
        },
        check_name_lobby: function(Lobby_with_name) {
            if (Lobby_with_name) {
                return true
            } else {
                return false
            }
        },
        check_knocking_lobby: function(Lobby_with_knocking) {
            if (Lobby_with_knocking) {
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
        start: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function() {
                const parent = $('#jitsi_meeting_placeholder');
                var div = document.createElement("div");
                div.id = "center_meeting";
                if (parent.length === 1) {
                    parent.append(div);
                }
                let name_lobby_on_off;

                const domain = parent.data("jitsi");
                const jwt_token = parent.data("jwt");
                const Lobby_with_knocking = parent.data('lobby_with_knocking');
                const Lobby_with_name = parent.data('lobby_with_name');

                //Check if there is a lobby.
                self.unicId = parent.data("link_suffix");
                self.rec_on_start = parent.data('start_recording');
                self.no_recording = parent.data('no_recording');
                self.Toggle_recording = false;
                // self.Lobby_on = self.check_lobby(Lobby_with_knocking, Lobby_with_name);

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
                if (parent.data("room_subject") == undefined) {
                    roomSubject = parent.data("meeting_subject")
                }

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
                    configOverwrite: {
                        // requireDisplayName = Name + Knocking
                        requireDisplayName: parent.data('lobby_with_knocking') ? true : false,
                        // prejoinPageEnabled = Name Only
                        prejoinPageEnabled: parent.data('lobby_with_name') ? true : false,
                        name_lobby_on_off: parent.data('lobby_with_name') ? true : false,
                        startWithAudioMuted: parent.data("microphone") ? false : true,
                        startWithVideoMuted: parent.data("webcam") ? false : true,
                        toolbarButtons: toolbarButtons,
                    },
                };
                console.log(parent.data('lobby_with_name'));

                self.api = new JitsiMeetExternalAPI(domain, options);

                self.api.executeCommand('subject', roomSubject);


                self._render_buttons(self.api, self.rec_on_start);

                // Removes the lingering jwt token from the dom tree.
                if (parent[0].attributes['data-jwt']) {
                    parent[0].removeAttribute('data-jwt')
                }

                // api.addEventListener('participantRoleChanged', function (event) {
                //     const lobby_with_knocking = parent.data('lobby_with_knocking')
                //     if (event.role === 'moderator' && lobby_with_knocking == "True") {
                //             api.executeCommand('toggleLobby', true)
                //     }
                // });
            });
        },
        //--------------------------------------------------------------------------
        // Private Methods
        //--------------------------------------------------------------------------
        _render_buttons: function (api, rec_on_start) {
            // let menu_html = `<div class='btn_holder' style='height:${this.$el.height()}px; width:auto; display:flex;'>   
            //                     <a id="lobby_btn" class='btn ${this.Lobby_on ? 'btn-on' : 'btn-off'} jitsi_button_lobby'>
            //                     ${this.Lobby_on ? '<i class="fa fa-lock" />' : '<i class="fa fa-unlock" />'}</a>
            //                     <a class='btn btn-room-react jitsi_button_room'>
            //                     <i class="fa fa-users" />
            //                     </a>
            //                     <a id="screen_btn" class='btn ${this.Lobby_on ? 'btn-on' : 'btn-off'} 
            //                      jitsi_button_fullscreen'>
            //                      <i class="fa fa-expand" /> </a>
            //                     </div>`
            //                     // ${self.menu_for_all}
            // let menu_for_all = `<div class='btn_holder_for_all' style='height:${this.$el.height()}px; width:auto; display:flex;'>   
            //                     <a id="screen_btn" class='btn ${this.Lobby_on ? 'btn-on' : 'btn-off'} 
            //                     jitsi_button_fullscreen'>
            //                     <i class="fa fa-expand" /> </a>
            //                     </div>`
                              
            let height = this.$el.height();

            api.addEventListener('participantRoleChanged', function (event) {
                const element = document.getElementById('btn_holder_id');
                // const lobby_with_knocking = document.getElementsByName('lobby_with_knocking')
                if (element){
                    element.remove();}
                if (event.role === 'moderator') {
                    // if(lobby_with_knocking == true){
                    //     api.executeCommand('toggleLobby', true)
                    // }
                        $('#center_meeting').append( `<div class='btn_holder' id='btn_holder_id' style='height:${height}px; width:auto; display:flex;'>
                                <a id="lobby_knocking_btn" class='btn ${this.Lobby_with_knocking ? 'btn-on' : 'btn-off'} jitsi_button_knocking_lobby'>
                                ${this.Lobby_with_knocking ? '<i class="fa fa-lock" />' : '<i class="fa fa-unlock" />'}
                                </a>
                                <a id="lobby_name_btn" class='btn ${this.Lobby_with_name ? 'btn-on' : 'btn-off'} jitsi_button_name_lobby'>
                                ${this.Lobby_with_name ? '<i class="fa fa-address-card" />' : '<i class="fa fa-address-card-o" />'}
                                </a>
                                <a id="screen_btn" class='btn ${this ? 'btn-on' : 'btn-off'} jitsi_button_fullscreen'>
                                    <i class="fa fa-expand" /> 
                                </a>
                                <a class='btn btn-room-react jitsi_button_room'>
                                <i class="fa fa-users" />
                                </a></div>`
                                )
                            
                } 
                else if (event.role !== 'moderator') {
                    // api.executeCommand('toggleLobby', true)
                    const element = document.getElementById('btn_holder_id');
                    if (element){
                        element.remove();}
                            $('#center_meeting').append( `<div class='btn_holder' id='btn_holder_id' style='height:${height}px; width:auto; display:flex;'>
                            <a id="screen_btn" class='btn ${this ? 'btn-on' : 'btn-off'} jitsi_button_fullscreen'>
                                <i class="fa fa-expand" />
                            </a></div>`
                        )
                }
            })
        },
        // _toggle_server_lobby: function(client_link_suffix, client_lobby_status) {
        //     let uri = `/video_meeting/${client_link_suffix}/toggle_lobby`
        //     let toggleMenu = ajax.jsonRpc(uri, 'call', {
        //         link_suffix: client_link_suffix,
        //         lobby_status: client_lobby_status
        //     })
        // },

        // _render_recording: function (rec_on_start) {
        //     if (this.no_recording) {
        //         return ""
        //     } else if (rec_on_start) {
        //         return "   <a id='rec_btn' class='btn btn-primary jitsi_button_rec'>Stop Recording!</a>"
        //     } else {
        //         return "   <a id='rec_btn' class='btn btn-success jitsi_button_rec'>Start Recording!</a>"
        //     }
        // },

        _toggle_knocking_lobby: function(e) {
            let button = $(e.target)
            let the_button = document.getElementById("lobby_knocking_btn");
            if (this.Lobby_with_knocking == "False") {
                this.api.executeCommand('toggleLobby', false)
                this.Lobby_with_knocking = false
                this._toggle_server_lobby(this.unicId, this.Lobby_with_knocking)

                the_button.classList.replace("btn-on", "btn-off");
                the_button.innerHTML = '<i class="fa fa-unlock" />';
            } else if (this.Lobby_with_knocking == "True") {
                this.api.executeCommand('toggleLobby', true)
                this.Lobby_with_knocking = true
                this._toggle_server_lobby(this.unicId, this.Lobby_with_knocking)

                the_button.classList.replace("btn-off", "btn-on");
                the_button.innerHTML = '<i class="fa fa-lock" />';
            }
        },

        _toggle_name_lobby: function(e) {
            // let button = $(e.target)
            // console.log(name_lobby_on_off);
            // console.log(this.check_name_lobby());
            let the_button = document.getElementById("lobby_name_btn");
            // console.log(the_button);
            console.log(the_button.classList.contains("btn_on"));
            console.log(the_button.classList.contains("btn_off"));
            console.log(the_button.classList);
            if (the_button.classList.contains("btn-on")) {
                // name_lobby_on_off = "false";
                console.log("off");
                the_button.classList.replace("btn-on", "btn-off");
                the_button.innerHTML = '<i class="fa fa-address-card-o" />';
            } else if (name_lobby_on_off == "false"){
                // this.the_button && 
                name_lobby_on_off = "true";
                console.log(name_lobby_on_off);
                console.log("on");
                the_button.classList.replace("btn-off", "btn-on");
                the_button.innerHTML = '<i class="fa fa-address-card" />';
            }
        },

        // _toggle_record: function(e) {
        //     let button = $(e.target)
        //     let the_button2 = document.getElementById("rec_btn");
        //     console.log(button)
        //     console.log(e)

        //     if (!this.Toggle_recording) {
        //         this.Toggle_recording = true;
        //         this.api.executeCommand('startRecording', {
        //             mode: 'file'
        //         })
        //         the_button2.classList.replace("btn-success", "btn-primary");
        //         the_button2.innerHTML = "<p>New Text</p>";
        //     } else if (this.Toggle_recording) {
        //         this.Toggle_recording = false;
        //         this.api.executeCommand('stopRecording', {
        //             mode: 'file'
        //         })
        //         the_button2.classList.replace("btn-primary", "btn-success");
        //         the_button2.innerHTML = "<i class='fa fa-users'></i>";
        //     }
        // },

        _toggle_room: function() {
            this.api.executeCommand('addBreakoutRoom', 'room')
        },
        _toggle_screen: function() {
            document.querySelector("#jitsiConferenceFrame0").requestFullscreen();
        }

    })
});
