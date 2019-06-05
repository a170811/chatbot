'use strict';

process.env.ACCESS_TOKEN = require('./myToken.js').ACCESS_TOKEN
let {PythonShell} = require('python-shell')

// Imports dependencies and set up http server
const
  fs = require('fs'),
  https = require('https'),
  express = require('express'),
  bodyParser = require('body-parser'),
  app = express().use(bodyParser.json()), // creates express http server
  { MessengerClient } = require('messaging-api-messenger'),
  client = MessengerClient.connect(process.env.ACCESS_TOKEN);

// const ngrok = require('ngrok');
// (async function(){
//     const url = await ngrok.connect(12345);
//     console.log(url);
// })();


// Creates the endpoint for our webhook
app.post('/webhook', (req, res) => {

  let body = req.body;

  // Checks this is an event from a page subscription
  if (body.object === 'page') {

    // Iterates over each entry - there may be multiple if batched
    body.entry.forEach(function(entry) {

      // Gets the message. entry.messaging is an array, but
      // will only ever contain one message, so we get index 0

      let webhook_event = entry.messaging[0];
      console.log(webhook_event)

      if(webhook_event.message.text && webhook_event.sender){
          const userId = webhook_event.sender.id;
          const text = webhook_event.message.text;

          let options = {
              mode: 'text',
              args:[text]
          }

          PythonShell.run('get.py', options, function (err, results) {
              if (err){
                console.log(err);
                res.sendStatus(404);
              }
              // results is an array consisting of messages collected during execution
              //console.log('results:', results[0]);
              client.sendText(userId, results[0]);
          });
      }

    });

    // Returns a '200 OK' response to all requests
    res.status(200).send('EVENT_RECEIVED');
  } else {
    // Returns a '404 Not Found' if event is not from a page subscription
    res.sendStatus(404);
  }

});

// Adds support for GET requests to our webhook
app.get('/webhook', (req, res) => {

  // Your verify token. Should be a random string.
  let VERIFY_TOKEN = "test"

  // Parse the query params
  let mode = req.query['hub.mode'];
  let token = req.query['hub.verify_token'];
  let challenge = req.query['hub.challenge'];

  // Checks if a token and mode is in the query string of the request
  if (mode && token) {

    // Checks the mode and token sent is correct
    if (mode === 'subscribe' && token === VERIFY_TOKEN) {

      // Responds with the challenge token from the request
      console.log('WEBHOOK_VERIFIED');
      res.status(200).send(challenge);

    } else {
      // Responds with '403 Forbidden' if verify tokens do not match
      res.sendStatus(403);
    }
  }
});


//app.listen(process.env.PORT || 12345, () => console.log('webhook is listening'));

// Sets server port and logs message on success
https.createServer({
    key: fs.readFileSync('./ssl/private.key'),
    cert: fs.readFileSync('./ssl/certificate.crt'),
    ca: fs.readFileSync('./ssl/ca_bundle.crt')
}, app)
.listen(process.env.PORT || 12345, () => console.log('webhook is listening'));
