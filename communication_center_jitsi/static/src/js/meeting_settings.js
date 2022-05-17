odoo.define("communication_center_jitsi.metting_settings.js", function (require) {
    "use strict";

    var publicWidget = require('web.public.widget')
    publicWidget.registry.jitsiMeetSettingsButtons = publicWidget.Widget.extend({
        selector: '#jitsi_meeting_placeholder',
        read_events: {
            'click .jitsi_button_lobby': '_toggle_lobby',
            'click .jitsi_button_rec': '_toggle_record',
            'click .jitsi_button_room': '_toggle_room',
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
                console.log("STARTINGGGGGGGG")

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
                const unicId = parent.data("link_suffix");

                //Check if there is a lobby.
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

                const options = {
                    roomName: unicId,
                    width: 1500,
                    height: 700,
                    parentNode: div,
                    jwt: jwt_token,
                    configOverwrite:
                    {
                        requireDisplayName: parent.data("lobby_with_name") == "True",
                        prejoinPageEnabled: parent.data("lobby_with_name") == "True",
                        startWithAudioMuted: parent.data("microphone_off") == "True",
                        startWithVideoMuted: parent.data("webcam_off") == "True",
                        toolbarButtons: toolbarButtons,
                    },
                };

                self.api = new JitsiMeetExternalAPI(domain, options);

                self._render_buttons(self.api);

                // Removes the lingering jwt token from the dom tree.
                if (parent[0].attributes['data-jwt']) {
                    parent[0].removeAttribute('data-jwt')
                }

                console.log("DONEEEEEE")
                // if (parent.data("start_recording") == "True") {
                //     console.log("REC");
                //     api.executeCommand('startRecording', {
                //         mode: 'file'
                //     })
                //     jitsi_button_rec.each(function () {
                //         this.innerText = "Stop Recording!";
                //         $(this).addClass('btn-primary');
                //         $(this).removeClass('btn-success');
                //         Toggle_recording = true;
                //     })
                // };

                // if (parent.data("lobby_with_knocking") == "True") {
                //     jitsi_button_lobby.each(function () {
                //         this.innerText = "Lobby on!";
                //         $(this).addClass('btn-success');
                //         $(this).removeClass('btn-primary');
                //     });
                //     api.addEventListener('participantRoleChanged', function (event) {
                //         console.log("participantRoleChanged", event);
                //         if (event.role === 'moderator') {
                //             api.executeCommand('toggleLobby', true)
                //             Lobby_on = true;
                //         }
                //     })
                // };
            });
        },
        //--------------------------------------------------------------------------
        // Private Methods
        //--------------------------------------------------------------------------
        _render_buttons: function (e) {
            let menu_html = "<div class='btn_holder'>"
                + "   <a class='btn btn-success jitsi_button_lobby'>Lobby on!</a>"
                + ( !this.no_recording ?  "   <a class='btn btn-success jitsi_button_rec' id='rec_btn'>Start Recording!</a>" : "" )
                + "   <a class='btn btn-success jitsi_button_room'>Create Room!</a>"
                + "</div>"

            this.api.addEventListener('participantRoleChanged', function (event) {
                console.log("participantRoleChanged", event);
                if (event.role === 'moderator') {
                    $('#center_meeting').append(menu_html)
                }
            })
        },

        _toggle_lobby: function (e) {
            console.log("TOGGLE LOBBY");
            let button = $(e.target)
            if (self.Lobby_on) {
                this.api.executeCommand('toggleLobby', false)
                self.Lobby_on = false

                button.text('Lobby off!');
                button.addClass('btn-primary');
                button.removeClass('btn-success');
            } else {
                this.api.executeCommand('toggleLobby', true)
                self.Lobby_on = true

                button.text('Lobby on!');
                button.addClass('btn-success');
                button.removeClass('btn-primary');
            }
        },

        _toggle_record: function (e) {
            let button = $(e.target)
            if (!this.Toggle_recording) {
                this.Toggle_recording = true;
                this.api.executeCommand('startRecording', {
                    mode: 'file'
                })
                button.text('Stop Recording!');
                button.addClass('btn-primary');
                button.removeClass('btn-success');
            }
            else if (this.Toggle_recording) {
                this.Toggle_recording = false;
                this.api.executeCommand('stopRecording', {
                    mode: 'file'
                })
                button.text('Start Recording!');
                button.addClass('btn-success');
                button.removeClass('btn-primary');
            }
        },

        _toggle_room: function () {
            console.log(this.api.getParticipantsInfo())
            this.api.executeCommand('addBreakoutRoom', 'room')
        }
    })
});

