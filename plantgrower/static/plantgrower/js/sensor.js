// When we're using HTTPS, use WSS too.
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";

var websocket = new WebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);

websocket.onmessage = function(message) {
  var data = JSON.parse(message.data);
  for (var key in data) {
    if (data.hasOwnProperty(key)) {
      try {
        document.getElementById(key).innerHTML = data[key];
      }
      catch (err) {
          console.warn("No " + key + " element to fill.");
      }
    }
  }
};

$('#top_lights').on('click', toggle_top_lights)
$('#side_lights').on('click', toggle_side_lights)
$('#fans').on('click', toggle_fans)
$('#pump').on('click', toggle_pump)

function toggle(device) {
    return websocket.send(JSON.stringify({ device: device }));
}

function toggle_top_lights() {
  toggle('TOP_LIGHTS');
}

function toggle_side_lights() {
  toggle('SIDE_LIGHTS')
}

function toggle_fans() {
  toggle('FANS')
}

function toggle_pump() {
  toggle('PUMP')
}
