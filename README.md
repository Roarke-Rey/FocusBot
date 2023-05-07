# FocusBot

## Overview
FocusBot is a Slack bot designed to assist users in efficiently managing their schedules, while also providing managers with a platform to monitor and manage their team members' schedules. The bot offers daily motivational quotes to keep users inspired and incorporates the Pomodoro technique to help users balance their work and rest periods, ultimately increasing their productivity and focus.

## Properties
* Schedule management 
    * add/update/delete tasks
    * all personal schedules at a glance
* Manager view
* Motivational quote every day
* Pomodoro techniques

## Developers
* Team: Focused Engineers
* Team Members
    * ANDREW JELSON    
        * Email: jelson9854@vt.edu
        * Github ID: Jelson9854
    * SHEAN KIM
        * Email: shean@vt.edu
        * Github ID: Shean50
    * SHREYAS PAWAR 
        * Email: shreyaspawar@vt.edu
        * Github ID: Roarke-Rey
*  Our Trello board is found at https://trello.com/b/kkHaxukr/focussed-engineers
 
## How To Run FocusBot
Start by cloning the github and using ***pip install -rrequirements.txt***
Running FocusBot requires the code owner to have a signing secret to add the bot to the server (we will email it to you becuase the secret gets taken off of GitHub). After obtaining the signing secret, you have to run a ngrok environment. Download ngrok and run the command ***ngrok http 5005***. Copy the forwarding address paste it in the slack API Event Subscriptions Request URL and add /slack/events (we will also email our slackAPI login). From there you can run install the bot onto your workspace and the bot will run properly 
## How To Run Test
Our test file is test.py. Running test.py will perform the assert statements to check that the bot is running properly.

## Example
### As a Team Manager
1) Send a direct message to FocusBot with the word ***schedule*** 
2) FocusBot will display a list of all the projects you can access, along with the following message
```
Please select the number for the project you want to see the schedule for:
[1] First Project
[2] FocusBot
[3] ...
```
3) You should select the number of the project that you would like to monitor
```
ex) 2
```
4) FocusBot will show the schedules of all team members who are included in that project
```
Found these tasks for the following users for project FocusBot
User: U056BJX4T1C
[1] Task: Demo    Due Date: 20230506
User: U051B4PF5JM
[1] Task: Finish Report    Due Date: 20230505
[2] Task: Demo    Due Date: 20230506
```
<img width="388" alt="Screenshot 2023-05-06 at 10 05 51 PM" src="https://user-images.githubusercontent.com/122955570/236653943-12c64594-e5c6-49bc-8f30-4df599d39acc.png">

### As a Team Member
#### View All Personal Schedules
1) Send a direct message to FocusBot with the word ***schedule*** 
2) FocusBot will display all of your schedules
```
[1] Project: FocusBot    Task: Finish Report    Due Date: 20230505
[2] Project: FocusBot    Task: Demo    Due Date: 20230506
```
<img width="652" alt="image" src="https://user-images.githubusercontent.com/57321224/236655268-3976e2b0-3377-4364-85fa-56e1fe42dc26.png">

#### Add a Schedule
1) Send a direct message to FocusBot with the word ***add_event*** 
2) Enter the task next in accordance to the format
```
Please enter the task be added in the format: 
Project_Name,TaskName,DueDate(YYYYMMDD)
```

3) You should type the schedule that you want to add
```
ex) FocusBot, Unit Test Development, 20230509
```
4) FocusBot will add your schedule, along with the following message
```
Added the task successfully
```
<img width="652" alt="image" src="https://user-images.githubusercontent.com/57321224/236655335-1a2e322a-bce6-4e16-9e6e-14abd35122f7.png">

#### Delete a Schedule
1) Send a direct message to FocusBot with the word ***delete_event*** 
2) FocusBot will display all of your schedules and ask you which one you would like to delete, along with the following message
```
Please enter the number of the task you want to delete:
[1] Project: FocusBot    Task: Finish Report    Due Date: 20230505
[2] Project: FocusBot    Task: Demo    Due Date: 20230506
[3] Project: FocusBot    Task: Unit Test Development    Due Date: 20230509
```
<img width="652" alt="image" src="https://user-images.githubusercontent.com/57321224/236655357-eeedfd81-ef86-4dc6-8994-ab2bc9cbd976.png">

#### How to use Pomodoro
1) Send a direct message to FocusBot with the command ***set_pomodoro*** to set the length of your sprint
2) Send a direct message to FocusBot with the command ***set_break*** to set the length of your break
3) Send a direct message to FocusBot with the command ***activate*** to get a list of activatable functions (Pomodoro is the only one implemented right now)
4) Send a direct message to FocusBot with the command ***pomodoro*** to have the bot run for your sprint and break time
5) Send a direct message to FocusBot with the command ***deactivate*** to get a list of activatable functions (Pomodoro is the only one implemented right now)
6) Send a direct message to FocusBot with the command ***pomodoro*** and the bot will stop pomodoro at the end of the next break time.

