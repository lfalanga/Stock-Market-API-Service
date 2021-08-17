from pyasn1.type.univ import Null
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
db = firebase.database()

# # Temporarily replace quote function
# def noquote(s):
#     return s
# pyrebase.pyrebase.quote = noquote

def login(email, password, cipher):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        apikey = get_apikey(cipher)
        return True, user["localId"], user["idToken"], apikey
        # CHECK IF USER'S DATA EXISTS IN FIREBASE #########
        # FORMAT JSON RESPONSE OUTPUT #########
    except Exception as e:
        #print(e)
        return False, Null, Null, Null

def signup(name, last_name, email, password, apikey):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        account_info = auth.get_account_info(user["idToken"])
        uid = account_info["users"][0]["localId"]
        data = {
            "name" : name,
            "lastName" : last_name,
            "email" : email,
            "apikey" : apikey
            }
        db.child("users").child(uid).set(data, user["idToken"])
        return True
    except Exception as e:
        print(e)
        return False

def get_apikey(cipher):
    try:
        user = auth.current_user
        uid = user["localId"]
        query = db.child("users").child(uid).get(user["idToken"])
        dict_user = query.val()
        apikey = dict_user["apikey"]
        decrypted_apikey = cipher.decrypt(apikey.encode("utf-8"))
        encrypted_apikey = cipher.encrypt(decrypted_apikey)

        # Returning a recylced encrypted apikey
        return encrypted_apikey.decode("utf-8")
    except Exception as e:
        print('Exception: ', e)
        return Null

def valid_apikey(uid, apikey, token, cipher):
    try:
        query = db.child("users").child(uid).get(token)
        dict_user = query.val()
        decrypted_logged_apikey = cipher.decrypt(apikey.encode("utf-8"))
        saved_apikey = dict_user["apikey"]
        decrypted_saved_apikey = cipher.decrypt(saved_apikey.encode("utf-8"))

        if decrypted_logged_apikey == decrypted_saved_apikey:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return Null

def log_request(uid, token, data):
    try:
        query = db.child("users").child(uid).get(token)
        dict_user = query.val()
        email = dict_user["email"]
        data["email"] = email
        data["timestamp"] = {".sv":"timestamp"}
        db.child("requests").child(uid).push(data, token)
        return True
    except Exception as e:
        print(e)
        return False

def get_logging_info_for_user(uid):
    try:
        query = db.child("requests").child(uid).get()
        dict_log = query.val()
        return dict_log
    except Exception as e:
        print(e)
        return Null

if __name__ == '__main__':
    pass