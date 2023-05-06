import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://focusbot-c6cfb-default-rtdb.firebaseio.com/"
})

# Initializing users
root = db.reference("/")

# Empyting all lists
# root.child("Users").set({})
# root.child("Managers").set({})

# Getting handles for users
users = db.reference("/Users/")
managers = db.reference("/Managers/")

# # Adding sample data
user1 = {
    "Name": "Shreyas", 
    "Projects": [ 
    {
        "Name": "FocusBot",
        "Tasks":[
        {
            "Name": "Sample Task1",
            "DueDate": "08032023"
        },
        {
            "Name": "Sample Task2",
            "DueDate": "09032023"
        }] 
    }]
}
user2 = {
    "Name": "Jelson", 
    "Projects": [ 
    {
        "Name": "FocusBot",
        "Tasks":[
        {
            "Name": "Sample Task3",
            "DueDate": "08032023"
        },
        {
            "Name": "Sample Task4",
            "DueDate": "09032023"
        }] 
    }]
}


managers.child("U051B4PF5JM").push({
    "Projects": [{
        "Name": "FocusBot",
        "Users": ["U056BJX4T1C","U051B4PF5JM"]
    }]
})

# users.push(user1)
# users.push(user2)
# managers.push(manager1)

# for key, value in users.get().items():
#     if value["Name"] == "Shreyas":
#         print(value["Projects"][0]["Tasks"])
        # value["Projects"].push()

# .order_by_child("Due Date")