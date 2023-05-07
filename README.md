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
 
## How To Run FocusBot
## How To Run Test
```
python test.py
```
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
[1] Task: Finish Report    Due Date: 20230505
[2] Task: Demo    Due Date: 20230506
```
#### Add a Schedule
1) Send a direct message to FocusBot with the word ***add_event*** 
2) FocusBot will display a list of all the projects you can access, along with the following message
```
Please enter the task be added in the format: 
Project_Name,TaskName,DueDate(YYYYMMDD)
```
3) You should type the schedule that you want to add
```
ex) FocusBot Meeting,FocusBot,20230505
```
4) FocusBot will add your schedule, along with the following message
```
Added the task successfully
```
#### Delete a Schedule
1) Send a direct message to FocusBot with the word ***delete_event*** 
2) FocusBot will display all of your schedules and ask you which one you would like to delete, along with the following message
```
Please enter the number of the task you want to delete:
[1] Task: Finish Report    Due Date: 20230505
[2] Task: Demo    Due Date: 20230506
```
