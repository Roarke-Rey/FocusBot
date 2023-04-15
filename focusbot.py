from __future__ import print_function

import firebase_admin
from flask import Flask, request, jsonify
from slackeventsapi import SlackEventAdapter
from firebase_admin import credentials, firestore, initialize_app

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from slack_sdk import WebClient
import datetime
from datetime import timedelta, datetime
from cal_setup import get_calendar_service

SLACK_TOKEN="<SLACK_TOKEN>"
SIGNING_SECRET="<SIGNING_SECRET>"

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)
client = WebClient(token=SLACK_TOKEN)

from slack_sdk.http_retry.builtin_handlers import RateLimitErrorRetryHandler
rate_limit_handler = RateLimitErrorRetryHandler(max_retry_count=-1) # To prevent duplicate answer
client.retry_handlers.append(rate_limit_handler)

@slack_event_adapter.on('message')
def message(payload):
    # print(payload)
    global previous_msg
    global tmp_list
    
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    
    ts = event.get('ts') # ts = timestamp
    texts=text.split()

    if texts[0] == "hi":
        previous_msg = texts[0]
        client.chat_postMessage(channel=channel_id, thread_ts=ts, text="Hello")
    elif texts[0] == "schedule":
        previous_msg = texts[0]
        start_list, event_list, evenId_list = google_calendar()
        res = parse_result(start_list, event_list)
        client.chat_postMessage(channel=channel_id, thread_ts=ts, text=res)
    elif texts[0] == "add_event":
        previous_msg = texts[0]
        # [format] add_event 10/31/2023/10:30 team meeting
        date=texts[1].split('/')
        time=date[3].split(':')
        summary=" ".join(texts[2:])
        start=datetime(int(date[2]), int(date[0]), int(date[1]), int(time[0]), int(time[1]))
        event_add(start, summary)
        client.chat_postMessage(channel=channel_id,thread_ts=ts, text="Event is successfully added")
    elif texts[0] == "delete_event":
        previous_msg = "delete_event"
        start_list, event_list, eventId_list = google_calendar()
        tmp_list=eventId_list
        res = "What event do you want to delete? Please input number\n"
        res += parse_result(start_list, event_list)
        client.chat_postMessage(channel=channel_id, thread_ts=ts, text=res)
    elif previous_msg == "delete_event":
        if texts[0] == "What":
            return
        previous_msg = ""
        num = int(texts[0])
        if len(tmp_list) < num:
            res = "Sorry, but it is out of range"
            client.chat_postMessage(channel=channel_id, thread_ts=ts, text=res) 
            return

        service = get_calendar_service()
        ind = num - 1
        eventId = tmp_list[ind]
        service.events().delete(calendarId='primary', eventId=eventId).execute()
        res = "Successfully delete the event"  
        client.chat_postMessage(channel=channel_id, thread_ts=ts, text=res)
    # elif texts[0] == "update_event": 
    # [SHEAN] Updating events is necessary?

def event_add(start, summary):
    service = get_calendar_service()
    start_time=start.isoformat()
    end_time = (start + timedelta(hours=1)).isoformat()
    calendar = {
        'summary': summary,
        'start': {"dateTime": start_time, 'timeZone': 'America/New_York'},
        'end': {"dateTime": end_time, 'timeZone': 'America/New_York'}
    }
    # [TODO] set end_time by user's command
    # [TODO] link firebase and find user's calendarId 
    event_result = service.events().insert(calendarId='primary',body=calendar).execute()

def firebase_init():
    if (not len(firebase_admin._apps)):
        cred = credentials.Certificate('firebaseKey.json')
        #default_app = initialize_app(cred)
        firebase_admin.initialize_app(cred,{
            'databaseURL' : 'https://focusbot-542f7.firebaseio.com'
        })
    
# def firebase_add():    
#     db = firestore.client()
#     collection_ref = db.collection('user')
#     auth='team_member'
#     calendarId=
#     collection_ref.add({'auth':'member',})

def parse_result(start_list, event_list):
    length = len(start_list)
    res=""
    for i in range(length):
        res += "[" + str(i+1) + "] "
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
        eventId_list=[]
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_list.append(start)
            event_list.append(event['summary'])
            eventId_list.append(event['id'])
        print('start_list: ',start_list) 
        print('event_list: ',event_list)
        return start_list, event_list, eventId_list

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    app.run(port=5002, debug=True)
    firebase_init()