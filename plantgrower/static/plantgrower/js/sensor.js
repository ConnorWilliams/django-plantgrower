// When we're using HTTPS, use WSS too.
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var stage_socket = new WebSocket(ws_scheme + '://' + window.location.host + "/plantgrower/");

stage_socket.onmessage = function(message) {
    document.getElementById('stage_time').innerHTML = message.data;
};
