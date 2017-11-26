function myfunc() {
    console.log("Hello!");
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new WebSocket(ws_scheme + '://' + window.location.host + "/plantgrower/");

    chatsock.onopen = function() {
           console.log("Connected!");
           $('#sensor').text("Connected!");
           chatsock.send("Connected!");
    };

    chatsock.onmessage = function(message) {
        console.log("Received Sock message!");
        console.log(message);
        $('#sensor').text(message.data);
    };

}
