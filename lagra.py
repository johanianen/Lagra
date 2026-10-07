#---------------------------------------------------------------------------
#Imports
import os,platform
import time
import json
import hashlib
from getpass import getpass

#---------------------------------------------------------------------------
#Constants

CLEAR = "cls" if platform.system() == "Windows" else "clear"
USERDATA_LOCATION = "userdata.json"

SELECTOR_LOGIN = "l"
SELECTOR_QUIT = "q"
SELECTOR_ADD_ITEM = "a"
SELECTOR_LIST_ITEMS = "l"
SELECTOR_TRY_AGAIN = "r"
SELECTOR_REGISTER = "r"

MESSAGE_WELCOME = f"""Welcome to Lagra (TM)

  {SELECTOR_LOGIN}) Log in
  {SELECTOR_REGISTER}) Register
  {SELECTOR_QUIT}) Quit"""

MESSAGE_QUIT = "Quitting..."
MESSAGE_GET_USERNAME = "Username: "
MESSAGE_GET_PASSWORD = "Password: "
MESSAGE_USER_MENU = """
Welcome {username}

These are your items

{items}
"""
MESSAGE_USER_ACTIONS = f"""Select an action

{SELECTOR_ADD_ITEM}) Add item
{SELECTOR_LIST_ITEMS}) List items
{SELECTOR_QUIT}) Log out
"""
MESSAGE_LOGOUT = "Logging out..."
MESSAGE_WAIT = "Press Enter to continue..."

ERROR_MENU = "Error: Invalid Option"
ERROR_LOGIN = f"""Error: Invalid username and/or password

{SELECTOR_TRY_AGAIN}) Try again
{SELECTOR_QUIT} Quit"""

CONSTANT_ACCESS = "access"
CONSTANT_WRITE = "write"
CONSTANT_ERROR = "error"

#---------------------------------------------------------------------------
#Global variables

user_input = ""
user_data = {}

#---------------------------------------------------------------------------
#Functions

def main_menu(option):
    if option == SELECTOR_LOGIN:
        login()
        return

    if option == SELECTOR_REGISTER:
        register()
        return

    if option == SELECTOR_QUIT:
        print(MESSAGE_QUIT)
        quit()

    else:
        return CONSTANT_ERROR

def login():
    user_data = access_userdata(CONSTANT_ACCESS, None)

    while True:
        username = input(MESSAGE_GET_USERNAME)
        password = password_hash(getpass(MESSAGE_GET_PASSWORD))

        if username in user_data and password in user_data[username].values():
            user_menu(username)
            return  
                
        else:
            print(ERROR_LOGIN)
            user_input = input()
            if user_input == SELECTOR_TRY_AGAIN:
                continue
            
            if user_input == SELECTOR_QUIT:
                return

            else:
                print(ERROR_MENU)
                return
                    


def user_menu(username):
    os.system(CLEAR)
    print(MESSAGE_USER_MENU.format(username=username, items=list_items(username)))
    while True:
        print(MESSAGE_USER_ACTIONS)
        user_input = input()

        if user_input == SELECTOR_ADD_ITEM:
            os.system(CLEAR)
            add_item(username)

        if user_input == SELECTOR_LIST_ITEMS:
            os.system(CLEAR)
            print(list_items(username))

        if user_input == SELECTOR_QUIT:
            os.system(CLEAR)
            print(MESSAGE_LOGOUT)
            return
        
        user_wait()
        os.system(CLEAR)

def add_item(username):
    user_data = access_userdata(CONSTANT_ACCESS, None)
    print("Add item: ")
    user_input = input()

    items = user_data[username]["items"]
    items.update({"item_" + str(len(items) + 1) : user_input})

    access_userdata(CONSTANT_WRITE, user_data)

    return True

def list_items(username):
    returnstr = ""
    i = 1
    user_data = access_userdata(CONSTANT_ACCESS, None)

    for item in user_data[username]["items"].values():
        returnstr += str(i) + ") " + item + "\n"
        i += 1

    return returnstr

def register():
    user_data = access_userdata(CONSTANT_ACCESS, None)

    print("Registering new user")

    username = input(MESSAGE_GET_USERNAME)
    password = password_hash(getpass(MESSAGE_GET_PASSWORD))

    user_data.update({
        username : {
        "id": str(len(user_data) + 1),
        "password": password,
        "items": {
            }
        }
    })

    access_userdata(CONSTANT_WRITE, user_data)

    print("New user {username} registered with id {id}".format(username=username, id=str(len(user_data))))


def access_userdata(option, userdata):
        if option == CONSTANT_ACCESS: 
            with open(USERDATA_LOCATION) as f: 
                return json.load(f)

        if option == CONSTANT_WRITE:
            data_to_write = json.dumps(userdata, indent=4)
            with open(USERDATA_LOCATION, "w") as f:
                f.write(data_to_write)

def user_wait():
    input(MESSAGE_WAIT)
    return

def password_hash(password):
    return hashlib.sha256(password.encode(encoding = 'UTF-8', errors = 'strict')).hexdigest()
            
#---------------------------------------------------------------------------
#Program execution start
while True:
    os.system(CLEAR)
    print(MESSAGE_WELCOME)

    user_input = input().strip()

    if main_menu(user_input) == CONSTANT_ERROR:
        print(ERROR_MENU)
        continue

    user_wait()
    

#---------------------------------------------------------------------------