from flask import Flask
from slackeventsapi import SlackEventAdapter
from slack_sdk import WebClient
 
SLACK_TOKEN="xoxb-4827200483924-4818142455750-7rndP438x9GV7rX2rJ6dfEyE"
SIGNING_SECRET="8b0bca5ef9d201847b4b79c98bbf7dd5"
 
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)
client = WebClient(token=SLACK_TOKEN)
client.chat_postMessage(channel='#flask-test',text='Hello World!')
 
 
if __name__ == "__main__":
    app.run(port=5002, debug=True)