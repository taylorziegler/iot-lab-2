document.onkeydown = updateKey;
document.onkeyup = resetKey;
window.onload = client;

var server_port = 65526;
var server_addr = "10.0.0.224";   // the IP address of your Raspberry PI
var client;

function client(){
    const net = require('net');
    client = net.createConnection({ port: server_port, host: server_addr })
    
    // get the data from the server
    client.on('data', (data) => {
        result = data.toString().split(",");
        document.getElementById("temperature").innerHTML = result[0];
        document.getElementById("obs_dist").innerHTML = result[1];
        document.getElementById("moving").innerHTML = result[2];
        console.log(data.toString());
        if (data == 'end') {
            client.end();
            client.destroy();
        }
        
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });


}

// Send data to the server
function send_data(keyCode) {
    if (client) {
        console.log(`Sending key code: ${keyCode}`);
        client.write(`${keyCode}\r\n`);
    }
}


// for detecting which key is been pressed w,a,s,d
function updateKey(e) {
    //e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        send_data("87");
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        send_data("83");
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        send_data("65");
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        send_data("68");
    }
}

// reset the key to the start state 
function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
}