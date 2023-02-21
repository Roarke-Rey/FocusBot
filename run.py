from __future__ import print_function

from flask import Flask
from slackeventsapi import SlackEventAdapter

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from slack_sdk import WebClient

SLACK_TOKEN="xoxb-4827200483924-4818142455750-7rndP438x9GV7rX2rJ6dfEyE"
SIGNING_SECRET="8b0bca5ef9d201847b4b79c98bbf7dd5"

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)
client = WebClient(token=SLACK_TOKEN)

from slack_sdk.http_retry.builtin_handlers import RateLimitErrorRetryHandler
rate_limit_handler = RateLimitErrorRetryHandler(max_retry_count=0)
client.retry_handlers.append(rate_limit_handler)

@slack_event_adapter.on('message')
def message(payload):
    # print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if text == "hi":
        client.chat_postMessage(channel=channel_id,text="Hello")
    elif text == "schedule":
        ts = event.get('ts') # ts = timestamp
        start_list, event_list = google_calendar()
        res = parse_result(start_list, event_list)
        print('res: ', res)
        client.chat_postMessage(channel=channel_id, thread_ts=ts, text=res)

def parse_result(start_list, event_list):
    length = len(start_list)
    res=""
    for i in range(length):
        res += start_list[i]
        res += "\n"
        res += event_list[i]
        if i != length-1:
            res += "\n\n"
    return res

def google_calendar():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        start_list=[]
        event_list=[]
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_list.append(start)
            event_list.append(event['summary'])
        print('start_list: ',start_list) 
        print('event_list: ',event_list)
        return start_list, event_list

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    app.run(port=5002, debug=True)