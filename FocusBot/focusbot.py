from flask import Flask, request, jsonify
from slackeventsapi import SlackEventAdapter

from firebase_admin import credentials, initialize_app

import time

from slack_sdk import WebClient
from operator import *
from firebase_admin import credentials, initialize_app
from firebase_admin import db

from generate import getQuote

SLACK_TOKEN=""
SIGNING_SECRET=""

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)
client = WebClient(token=SLACK_TOKEN)

from slack_sdk.http_retry.builtin_handlers import RateLimitErrorRetryHandler
rate_limit_handler = RateLimitErrorRetryHandler(max_retry_count=-1) # To prevent duplicate answer
client.retry_handlers.append(rate_limit_handler)

# Keeping track of the previous message for some prompts
previous_msg = ""
pomo = 0.5
bTime = 0.5
pomoActive = False
"""
Currently Daily is set to a Boolean because our code isnt permanently hosted. We implement
a function to set the time later on but it would have to be edited when permanently hosted
"""
daily = True

@slack_event_adapter.on('message')
def message(payload):
    global previous_msg
    global max_index
    global daily
    global pomoActive
    global bTime
    global pomo
    
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    
    # When we deploy, we would use this following code
    ts = event.get('ts') # ts = timestamp
    #if(daily = time.asctime(time.localtime(time.time()))):
    #    client.chat_postMessage(channel=channel_id, thread_ts=ts, text="Good Morning. Lets get our workday started with a motivational quote"+getQuote())    
    while daily:
        client.chat_postMessage(channel=channel_id, thread_ts=ts, text="Good Morning. Lets get our workday started with a motivational quote. "+getQuote())
        daily = False
    user_text = text
    first_word = text.split()[0]

    # The firebase reference for manager root
    manager_reference = db.reference("/Managers/").get()
    manager_list = []
    if manager_reference != None:
        for key, value in manager_reference.items():
            manager_list.append(key)

    if first_word == "hi":
        previous_msg = user_text
        client.chat_postMessage(channel=user_id, thread_ts=ts, text="Hello")

    # The following code implements the manager view
    elif user_id in manager_list:
        # To get the list of all projects for the manager
        if first_word == "schedule":
            project_names = get_projects_for_manager(user_id)
            index = 1
            response = "Please select the number for the project you want to see the schedule for:\n"
            for project in project_names:
                response += "[{0}] {1}".format(index, project)
            client.chat_postMessage(channel=user_id, thread_ts=ts, text=response)
            max_index = len(project_names)
            previous_msg = "schedule"

        # To get the schedule of all users working in that project
        elif previous_msg == "schedule" and (not user_text.startswith("Please")):
            user_index = int(user_text.strip())
            previous_msg = ""
            # Checking for the index to be in the correct range of number of projects
            if user_index > 0 and user_index <= max_index:
                project_names = get_projects_for_manager(user_id)
                project_name = project_names[user_index-1]
                user_list = get_users_for_project(project_name, user_id)
                response = "Found these tasks for the following users for project {}\n".format(project_name)
                for user in user_list:
                    response += "User: {}\n".format(user)
                    response += get_project_schedule_from_user(project_name, user)
                client.chat_postMessage(channel=user_id, thread_ts=ts, text=response)
            else:
                response = "Invalid number for the project entered"
                client.chat_postMessage(channel=user_id, thread_ts=ts, text=response)
            max_index = 0

    # The way to add a task for the user
    elif first_word == "add_event":
        previous_msg = "add_event"
        response = "Please enter the task be added in the format:\nProject_Name,TaskName,DueDate(YYYYMMDD)"
        client.chat_postMessage(channel=user_id, thread_ts=ts, text=response)

    # Follow up check for the task added to be in the correct format
    elif previous_msg == "add_event" and (not user_text.startswith("Please")):    # The "Please" check because slack double runs the if loop
        if (check_format(text)):
            data = get_data_from_message(text)
            users = db.reference("/Users/")
            users.child(user_id).push(data)
            response = "Added the task successfully"
        else:
            response = "Invalid format for the task"
        client.chat_postMessage(channel=user_id, thread_ts=ts, text=response)
        previous_msg = ""

    # Way to view the schedule for the user
    elif user_text == "schedule":
        response, max_index = get_response_from_user_schedule(user_id)
        client.chat_postMessage(channel=user_id, thread_ts=ts, text=response)
    
    # Delete task startup by the user
    elif user_text == "delete_event":
        response, max_index = get_response_from_user_schedule(user_id)
        if response.startswith("Did not") or response.startswith("No schedule"):
            final_response = response
            previous_msg = ""
        else:
            final_response = "Please enter the number of the task you want to delete:\n" + response
            previous_msg = "delete_event"
        client.chat_postMessage(channel=user_id, thread_ts=ts, text=final_response)      
    
    # Follow up check for the delete task 
    elif previous_msg == "delete_event" and (not user_text.startswith("Please")) :
        user_index = int(user_text.strip())
        # Checking if the delete index is in range of the task count
        if user_index <= max_index and user_index > 0:
            user_data = find_user_data(user_id)
            index = 1
            # Sorting to get in descending order of date
            for key, task in sorted(user_data.items(),key=lambda x:getitem(x[1],'DueDate')):
                if index == user_index:
                    del user_data[key]
                    break
                index += 1
            users = db.reference("/Users/")
            users.child(user_id).set(user_data)
            response = "Task deleted successfully"
            client.chat_postMessage(channel=user_id, thread_ts=ts, text=response)
        else:
            response = "Invalid number for the task entered"
            client.chat_postMessage(channel=user_id, thread_ts=ts, text=response)
        previous_msg = ""

    # Motivational Quote for the user
    elif first_word == "quote":
        previous_msg = first_word
        client.chat_postMessage(channel=channel_id, thread_ts=ts, text=getQuote())

    # A way of starting of setup for Pomodoro sprint time
    elif first_word == "set_pomodoro":
        previous_msg = first_word
        client.chat_postMessage(channel=channel_id, thread_ts=ts, text="How long would you like your Pomodoro sprint to be?")
    
    # A way of starting of setup for the Break time for Pomodoro
    elif first_word == "set_break":
        previous_msg = first_word
        client.chat_postMessage(channel=channel_id, thread_ts=ts, text="How long would you like your Pomodoro break to be?")

    # Setup for activating of functions
    elif first_word == "activate":
        previous_msg = "activate"
        client.chat_postMessage(channel=channel_id, thread_ts=ts, text="What function would you like to activate? Available functions are: Pomodoro")

    # Completion of activation for the pomodoro technique
    elif first_word == "pomodoro":
        if previous_msg == "activate":
            previous_msg = ""
            pomoActive = True
            pomodoro(channel_id, ts)
        elif previous_msg == "deactivate":
            previous_msg = first_word
            pomoActive = False
            client.chat_postMessage(channel=channel_id, thread_ts=ts, text="Pomodoro is deactivated")

    # Deactivating the functioning of the pomodoro technique
    elif first_word == "deactivate":
        previous_msg = first_word
        client.chat_postMessage(channel=channel_id, thread_ts=ts, text="What function would you like to deactivate? Available functions are: Pomodoro")

    # Setting up the start up time for the work day
    elif first_word == "set_daily":
        previous_msg = first_word
        client.chat_postMessage(channel=channel_id, thread_ts=ts, text="What time would you like the daily message to be sent (in HH:MM:SS format)?")
    elif previous_msg == "set_daily" and (not user_text.startswith("Please")):
        if (check_time(text)):
            pass
            """
            daily = text
            """


def check_time(message):
    time_list = [word for word in message.split(":")]
    return len(time_list) == 3
    

def check_format(message):
    '''
    Validates the format of the add_event text of the user
    '''
    formatted_list = [word.strip() for word in message.split(",")]
    date = formatted_list[-1]
    return len(formatted_list) == 3 and len(date) == 8

def get_data_from_message(message):
    '''
    This function traverses the user given message to separate the task details
    '''
    formatted_list = [item.strip() for item in message.split(",")]
    return {"ProjectName": formatted_list[0],
            "TaskName": formatted_list[1],
            "DueDate": formatted_list[2]}

def get_response_from_user_schedule(user_id):
    '''
    Gets the entire schedule for the user from database
    '''
    user_data = find_user_data(user_id)
    if user_data == "":
        response = "Did not find the user in the database"
        index = 0
    elif user_data == "NA":
        response = "No schedule found for this user"
        index = 0
    else: 
        response = ""
        index = 1
        # Sorting to get in descending order of date
        for key, task in sorted(user_data.items(),key=lambda x:getitem(x[1],'DueDate')):
            response += "[{0}] Project: {1}\tTask: {2}\tDue Date: {3}\n".format(index, task["ProjectName"], task["TaskName"], task["DueDate"])
            index += 1
    return response, index-1

def get_project_schedule_from_user(project_name, user_id):
    '''
    Gets all tasks for a particular project for a particular user
    '''
    user_data = find_user_data(user_id)
    if user_data == "":
        response = "Did not find the user in the database"
    elif user_data == "NA":
        response = "No schedule found for this user"
    else: 
        response = ""
        index = 1
        for key, task in sorted(user_data.items(),key=lambda x:getitem(x[1],'DueDate')):
            if task["ProjectName"] == project_name:
                response += "[{0}] Task: {1}\tDue Date: {2}\n".format(index, task["TaskName"], task["DueDate"])
                index += 1
    if response == "":
        response = "Did not find any tasks for this user for the project\n"
    return response

def get_projects_for_manager(user_id):
    '''
    Returns a list of all the projects for a particular manager
    '''
    user_data = db.reference("/Managers/").child(user_id).get()
    project_names = []
    for key, value in user_data.items():
        for project in value["Projects"]:
            project_names.append(project["Name"])
    return project_names

def get_users_for_project(project_name, user_id):
    '''
    Returns a list of all users involved in a particular project
    '''
    user_data = db.reference("/Managers/").child(user_id).get()
    user_list = []
    for key, value in user_data.items():
        for project in value["Projects"]:
            if project["Name"] == project_name:
                user_list = project["Users"]
    return user_list

def find_user_data(user_id):
    '''
    Returns all the user data (tasks) for a particular user
    '''
    users = db.reference("/Users/")
    all_users_data = users.get()
    user_data = ""
    if all_users_data == None:
        return "NA"
    for key, value in all_users_data.items():
        if key == user_id:
            value = users.child(user_id).get()
            user_data = value
            break
    return user_data

    
def firebase_init():    
    '''
    Initializes the firebase database for the project
    '''
    cred = credentials.Certificate("firebase_credentials.json")
    initialize_app(cred, {
        "databaseURL": "https://focusbot-c6cfb-default-rtdb.firebaseio.com/"
    })

def pomodoro(channel_id, ts):
    '''
    For Demo Purposes - Runs the code for a while with breaks
    '''
    while pomoActive:
        client.chat_postMessage(channel=channel_id, thread_ts=ts, text="Starting Pomodoro for "+str(pomo)+" minutes")
        time.sleep(pomo*60)
        client.chat_postMessage(channel=channel_id, thread_ts=ts, text="Congratulations on completing a sprint. Take a break for "+str(bTime)+" minutes")
        time.sleep(bTime*60)

if __name__ == '__main__':
    firebase_init()
    app.run(port=5005, debug=True)
