const http = require('http');
const static = require('node-static');
const file = new static.Server('./');

var mqtt = require('mqtt')
var options = {
    port: 3000, 
    host: 'mqtt://m11.cloudmqtt.com',
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

const server = http.createServer((req,res) => {
    req.addListener('end', () => file.serve(req, res)).resume();
  });
  const port = 3000;
  server.listen(port, () => console.log(`Server running at http://localhost:${port}`));