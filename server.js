var express = require('express');
var path = require('path');
var bodyParser = require('body-parser');
var app = express();
var mqtt = require('mqtt')

var data = [{}]; // empty JSON object

var options = {
    port: 17657, 
    host: 'mqtt://m16.cloudmqtt.com',
    clientId: 'mqttjs_' + Math.random().toString(16).substr(2,8),
    username: 'hgyfcdvp',
    password: '7xO7C0uC6s-U',
    keepalive: 60,
    reconnectPeriod: 1000,
    protocolId: 'MQIsdp',
    protocolVersion: 3,
    clean: true,
    encoding: 'utf8'
};

var client = mqtt.connect('mqtt://m16.cloudmqtt.com', options);
client.on('connect', function() { 
    console.log('mqtt connected');
    data = [{}];
    client.subscribe('Calvin/Parkinglot14/row1/#', function() {
        client.on('message', function(topic, message, packet) {
            console.log('Received '+ message + " on " + topic + " ");
            if (message == "available") {
                data += 0; 
            } else {
                data +=1; 
            }
        });
    });
})
const http = require('http');
const static = require('node-static');
const file = new static.Server('./');



const server = http.createServer((req,res) => {
    req.addListener('end', () => file.serve(req, res)).resume();
  });
  const port = 3000;
  server.listen(port, () => console.log(`Server running at http://localhost:${port}`));