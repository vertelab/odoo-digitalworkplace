                                                                     
odoo.define("communication_center_jitsi/static/src/js/meeting_settings.js", function (require) {
    "use strict";

    const domain = 'meet.vertel.se';
    const options = {
        roomName,
    };
        
    const api = new JitsiMeetExternalAPI(domain, options);
    
    api.addEventListener('participantRoleChanged', function (event) {
        if(event.role === 'moderator') {
            api.executeCommand('toggleLobby', true);
        }
    }
    )
});
            
            
            //class MettingSettings {
       /* _onTrackingStatusClick(event) {
            var tracking_email_id = $(event.currentTarget).data("tracking");
            event.preventDefault();
            return this.env.bus.trigger("do-action", {
                action: {
                    type: "ir.actions.act_window",
                    view_type: "form",
                    view_mode: "form",
                    res_model: "mail.tracking.email",
                    views: [[false, "form"]],
                    target: "new",
                    res_id: tracking_email_id,
                },
            });
        }*/
    //}
    //MessageList.components.Message = MettingSettings;
//});


//https://meet.vertel.se/external_api.js