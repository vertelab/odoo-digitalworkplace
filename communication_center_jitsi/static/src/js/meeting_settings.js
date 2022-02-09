    console.log("start");
    odoo.define("communication_center_jitsi.metting_settings.js", function (require) {
    "use strict";

    console.log("after start");
    var rpc = require("web.rpc"); //maby create a funktion insted off APIsettings or add .this

    //console.log(rpc);
    /*const APIsettings = rpc.query({
        model: "ir.config_parameter",
        method: "get_param",
        args: ["communication_center_jitsi"],
    });*/
    console.log("sup")

    $('document').ready(function (event) {
        console.log("going");
        var div = document.createElement("div");
        const domain = 'meet.jit.si'; //TODO: fetch url from the feld thats in setings in odoo
        const options = {
            roomName: 'JitsiMeetAPIExample4567',
            width: 700,
            height: 700,
            parentNode: div,
        };
        const api = new JitsiMeetExternalAPI(domain, options);

        console.log("maby?");
        api.addEventListener('participantRoleChanged', function (event) {
            if(event.role === 'moderator') {
                api.executeCommand('toggleLobby', true);
            }
        })

        console.log("Hi!!")
        console.log(api)
        console.log("Hi2!!")
        console.log(div)
    
    });
    console.log("wait for it")

    async function name() {
        const _super = this_super.bind(this);

        console.log("go!");
        var data = await this.rpc({
            model: 'calendar.event',  //namnet på filen (py)
            method: 'button_test', //namnet på funktionen i filen
        });

        //vad ska hända
        alert("SUP!!!");
    };
    return _super(something)

});
console.log("end");
