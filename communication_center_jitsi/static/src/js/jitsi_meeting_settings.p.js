    odoo.define("web.assets_backend.js", function (require) {
    "use strict";

    JitsiMeetJS.init();

    var connection = new JitsiMeetJS.JitsiConnection(null, null, options);

    connection.addEventListener(JitsiMeetJS.events.connection.CONNECTION_ESTABLISHED, onConnectionSuccess);
    connection.addEventListener(JitsiMeetJS.events.connection.CONNECTION_FAILED, onConnectionFailed);
    connection.addEventListener(JitsiMeetJS.events.connection.CONNECTION_DISCONNECTED, disconnect);

    connection.connect();

    room = connection.initJitsiConference("conference1", confOptions);
    room.on(JitsiMeetJS.events.conference.TRACK_ADDED, onRemoteTrack);
    room.on(JitsiMeetJS.events.conference.CONFERENCE_JOINED, onConferenceJoined);

    JitsiMeetJS.createLocalTracks().then(onLocalTracks);

    room.join();

    const api = new JitsiMeetExternalAPI(domain, options);

    });
