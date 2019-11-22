/*
 * @Description: websocket（端口是80，websocket不是socket）
 * @Version: 1.0
 * @Autor: lhgcs
 * @Date: 2019-11-22 16:04:15
 * @LastEditors: lhgcs
 * @LastEditTime: 2019-11-22 16:09:43
 */

const WebSocket = require("ws");

client = {};
url="ws://127.0.0.1:80";


function connect(url, callback = () => {}) {
    logger.info("Websocket start");

    client = new WebSocket(url);
    // 没触发
    client.on('open', function(evt) {
        console.log("open");
    });

    client.on('message', function(data) {
        console.log("messagw");
    });

    // 服务器断开时，触发error/close
    client.on('error', function(err) {
        console.log("error");
        console.log(err);
        client.close();
    });

    client.on('close', function(evt) {
        console.log("close");
    });

    logger.info("Websocket end");
};


let WebSocketClient = require('websocket').client;
let client = new WebSocketClient();
 
client.on('connectFailed', function(error) {
    console.log('Connect Error: ' + error.toString());
});

client.on('connect', function(connection) {
    console.log('WebSocket Client Connected');
    // 服务器断开时，触发error/close
    connection.on('error', function(error) {
        console.log("Connection Error: " + error.toString());
    });

    connection.on('close', function() {
        console.log('echo-protocol Connection Closed');
    });

    connection.on('message', function(message) {
        if (message.type === 'utf8') {
            console.log("Received: '" + message.utf8Data + "'");
        }
    });
    
    function sendNumber() {
        if (connection.connected) {
            let number = Math.round(Math.random() * 0xFFFFFF);
            connection.sendUTF(number.toString());
            setTimeout(sendNumber, 1000);
        }
    }
    sendNumber();
});
 
client.connect(url, 'echo-protocol');
