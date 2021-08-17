from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
import secrets
import auth
import avapi
import fernet

cipher = fernet.get_ecryption_key()
myapi = Flask(__name__)
limiter = Limiter(myapi, key_func=get_remote_address)

"""
### GLOBAL FLASK-LIMMITER CONFIGURATION #########
limiter = Limiter(
  app,
  key_func=get_remote_address,
  default_limits=["200/day", "50/hour"]
)
###
"""

@myapi.route("/")
@limiter.limit("1/second")
@limiter.limit("10/minute")
def index():
  return { "message" : "Welcome to my Stock Market API Service!" }

@myapi.post("/login")
@limiter.limit("1/second")
@limiter.limit("10/minute")
def login():
    try:
        if request.is_json:
            obj_req = request.get_json()
            email = obj_req["email"]
            password = obj_req["password"]
            data = {
                "email" : email,
                }
            logged_in, uid, token, apikey = auth.login(email, password, cipher)
            if logged_in:
                data["loggedIn"] = True
                data["apikey"] = apikey
                data["userId"] = uid
                data["token"] = token
                return jsonify(data)
            else:
                return make_error(501, 6, "The request method is not supported by the server and cannot be handled.", '/login')
        else:
            return make_error(415, 5, "Request must be JSON", '/login')
    except:
        return make_error(501, 4, "The request method is not supported by the server and cannot be handled.", '/login')

@myapi.post("/signup")
@limiter.limit("1/second")
@limiter.limit("10/minute")
def signup():
    try:
        if request.is_json:
            obj_req = request.get_json()
            name = obj_req["name"]
            last_name = obj_req["lastName"]
            email = obj_req["email"]
            password = obj_req["password"]
            apikey = secrets.token_urlsafe(12)
            encrypted_apikey = cipher.encrypt(apikey.encode())
            data = {
                "name" : name,
                "lastName" : last_name,
                "email" : email
                }
            signed_up = auth.signup(name, last_name, email, password, encrypted_apikey.decode("utf-8"))
            if signed_up:
                data["message"] = "User created succesfully."
                data["createdUser"] = True
                return jsonify(data)
            else:
                return make_error(501, 3, "The request method is not supported by the server and cannot be handled.", '/signup')
        return make_error(415, 2, "Request must be JSON", '/signup')
    except Exception as e:
        print(e)
        return make_error(501, 1, "The request method is not supported by the server and cannot be handled.", '/signup')

# The actual decorator function
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        try:
            uid = request.headers["userId"]
            apikey = request.headers["apikey"]
            token = request.headers["token"]
            if apikey:
                if auth.valid_apikey(uid, apikey, token, cipher):
                    return view_function(*args, **kwargs)
                else:
                    return make_error(501, 9, "The request method is not supported by the server and cannot be handled.", '/smi')
            else:
                return make_error(501, 8, "The request method is not supported by the server and cannot be handled.", '/smi')
        except:
            return make_error(501, 7, "The request method is not supported by the server and cannot be handled.", '/smi')
    return decorated_function

@myapi.get("/smi")
@limiter.limit("1/second")
@limiter.limit("10/minute")
@require_appkey
def get_stock_market_info():
    try:
        symbol = request.args["symbol"]
        data = avapi.get_stock_market_info(symbol)
        log = { 
            "method" : "GET",
            "endpoint" : "/smi",
            "symbol" : symbol
            }
        uid = request.headers["userId"]
        token = request.headers["token"]
        auth.log_request(uid, token, log)
        return jsonify(data)
    except Exception as e:
        print(e)
        return make_error(501, 10, "The request method is not supported by the server and cannot be handled.", '/smi')

@myapi.get("/log")
@limiter.limit("1/second")
@limiter.limit("10/minute")
def get_logging_info():
    try:
        uid = request.args["userId"]
        log = auth.get_logging_info_for_user(uid)
        return jsonify(log)
    except:
        return make_error(501, 11, "The request method is not supported by the server and cannot be handled.", '/log')

def make_error(status_code, sub_code, message, action):
    response = jsonify({
        'status': status_code,
        'sub_code': sub_code,
        'message': message,
        'action': action
    })
    response.status_code = status_code
    return response

@myapi.errorhandler(429)
def ratelimit_handler(e):
  return { "message" : "You have exceeded your rate-limit." }

if __name__ == '__main__':
    load_dotenv()
    myapi.run(debug=True)