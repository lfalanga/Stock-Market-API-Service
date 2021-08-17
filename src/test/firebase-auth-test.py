import sys
from os import name
import pyrebase

config = {
    "apiKey": "AIzaSyDCso0cqFCoAXX-hSzI41vb-2VHx_jtEX4",
    "authDomain": "stock-market-api-service.firebaseapp.com",
    "projectId": "stock-market-api-service",
    "storageBucket": "stock-market-api-service.appspot.com",
    "messagingSenderId": "558236191454",
    "appId": "1:558236191454:web:8d9d97cbb894bf51f2104f",
    "measurementId": "G-F8LTE8XB61",
    "databaseURL" : "https://stock-market-api-service-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

def signup():
    print("### SIGNING UP #########")
    name = input("Enter your name: ")
    last_name = input("Enter your last name: ")
    email = input("Enter your email address: ")
    password = input("Enter your password: ")
    # REGEX FOR PASSWORDS #########
    try:
        if create_user(name, last_name, email, password):
            print("User succesfully created.")
            ask = input("Do you want to log in now? [y/n]: ")
            if ask == "y":
                login()
            elif ask == "n":
                print("Program terminated.") 
    except: 
        print("Something went wrong.")
        e = sys.exc_info()
        print(e)
        # USER EXISTS #########

def create_user(name, last_name, email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        account_info = auth.get_account_info(user["idToken"])
        local_id = account_info["users"][0]["localId"]
        password_hash = account_info["users"][0]["passwordHash"]
        data = {
            "name" : name,
            "lastName" : last_name
            }
        db = firebase.database()
        db.child("users").child(local_id).set(data, user["idToken"])
        return True
    except: 
        print("Something went wrong.")
        e = sys.exc_info()
        print(e)
        return False

def login():
    print("### LOGGING IN #########")
    email = input("Enter your email address: ")
    password = input("Enter your password: ")
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        account_info = auth.get_account_info(login["idToken"])
        local_id = account_info["users"][0]["localId"]
        print("Succesfully logged in.")
        ##print(auth.get_account_info(account_info)
        # CHECK IF USER'S DATA EXISTS IN FIREBASE #########
        # FORMAT JSON RESPONSE OUTPUT #########
    except:
        print("Something went wrong.")
        e = sys.exc_info()
        print(e)
        # USER DOESN'T EXIST #########
        # WRONG PASSWORD #########

if __name__ == '__main__':
    answer = input("Are you a new user? [y/n]: ")
    if answer == "y":
        signup()
    elif answer == "n":
        login()