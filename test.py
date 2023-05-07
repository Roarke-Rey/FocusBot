import slack
from flask import Flask
from slackeventsapi import SlackEventAdapter

SLACK_TOKEN = "xoxb-5035002541524-5018019441527-QMBboxW4lCQa9PYeWdXQIjrp"
SIGNING_SECRET = "0765bee7c57d9ce966c3577af2cb9643"
 
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)
 
client = slack.WebClient(token=SLACK_TOKEN)
 
@ slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
 
    if text == "hi":
        return "Hello"
    elif text == "motivation":
        client.chat_postEphemeral(channel=channel_id, user=user_id, text="Be like Shreyas")
        return

def test_hello_message():
    payload = {'token': 'nBo2GSZmXkdJ5uZ8K9IZ692N', 'team_id': 'T051102FXFE', 'context_team_id': 'T051102FXFE', 'context_enterprise_id': None, 'api_app_id': 'A050VHFBXNH', 'event': {'client_msg_id': '54a4276b-844d-4f29-9ea5-e7ee48867f4d', 'type': 'message', 'text': 'hi', 'user': 'U051B4PF5JM', 'ts': '1683317838.594899', 'blocks': [{'type': 'rich_text', 'block_id': 'Fa+', 'elements': [{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'hi'}]}]}], 'team': 'T051102FXFE', 'channel': 'C050YG1GQQJ', 'event_ts': '1683317838.594899', 'channel_type': 'channel'}, 'type': 'event_callback', 'event_id': 'Ev056E9NFHLM', 'event_time': 1683317838, 'authorizations': [{'enterprise_id': None, 'team_id': 'T051102FXFE', 'user_id': 'U050J0KCZFH', 'is_bot': True, 'is_enterprise_install': False}], 'is_ext_shared_channel': False, 'event_context': '4-eyJldCI6Im1lc3NhZ2UiLCJ0aWQiOiJUMDUxMTAyRlhGRSIsImFpZCI6IkEwNTBWSEZCWE5IIiwiY2lkIjoiQzA1MFlHMUdRUUoifQ'}
    assert message(payload) == "Hello", "fail"

# More test cases were not added as they would basically just test the if else statements

if __name__ == "__main__":
    test_hello_message()

'''
There was no Slack testing API to be found for Python modules, especially considering that the app was also run on Flask.
Hence, for the unit test cases for the project, a separate file of Python tests was developed, 
which tested on a slightly modified deployment project file,
simulating the same functioning of the original project,
but had changes made to it so that it could be tested using unit tests in Python. 
'''