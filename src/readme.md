# Stock Market API Service
A simple Flask REST API implementation with Alpha Vantage Service web service integration.
For Authentication purposes and also, users and logging information, I have used Firebase service.

In order to maintain the repository clean, I've deleted unnecessary files from the project. Inside the file requirements.txt you can find all necessary packages you need to install for running the application.

Inside the folder "src" you will find the 4 main files needed for running the API server.

I recommend using Postman for testing purposes. But there are other tools available on the web.

## myapi.py
This is the main file of the project. It contains the Flask implementation, and here you can find the defined endpoints:

### @myapi.route("/")
An endpoint defined just for testing purposes.

### @myapi.post("/login")
This is a POST endpoint for logging in into the application.
#### Example Request:
POST http://localhost:5000/login
Body:
{
    "email": "new@new.com",
    "password": "123456"
}
#### Example Response:
Body:
{
    "apikey": "gAAAAABhGyfo19Tdf5H2SqnsyF3XPRH1sf3ZaBnZ2srolXeWw25lvdjQPOtAU99SG6fQmECZmLjHMM7YhSJ6sWiEtHXpBcPtBozKa80MUs0WTm-HXtrIVRo=",
    "email": "new5@new5.com",
    "loggedIn": true,
    "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjM2NGU4NTQ1NzI5OWQ5NzIxYjczNDQyZGNiNTQ3Y2U2ZDk4NGRmNTkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc3RvY2stbWFya2V0LWFwaS1zZXJ2aWNlIiwiYXVkIjoic3RvY2stbWFya2V0LWFwaS1zZXJ2aWNlIiwiYXV0aF90aW1lIjoxNjI5MTY5NjQwLCJ1c2VyX2lkIjoiY1RmUE1INDV3SVlKcUxMWnBNdHhOVWxpRm1YMiIsInN1YiI6ImNUZlBNSDQ1d0lZSnFMTFpwTXR4TlVsaUZtWDIiLCJpYXQiOjE2MjkxNjk2NDAsImV4cCI6MTYyOTE3MzI0MCwiZW1haWwiOiJuZXc1QG5ldzUuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm5ldzVAbmV3NS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.Ym2KDfe9By_HMvoXIsyrbJ_I3A9peNXOVvh-QJXFOWGDtzNYYPpNstShFmWYnSTpP1r3nnXXo23EH1FIu-wMeMFYrG1BfrKQYPdDsdLXzCCOZKl_Mu5ApWLWXEwoP9Mo-PmTzM7CHQ6A4UkPIE06VguKPBsryT2K-BGjyNHxXkZmcdIdeCzWidU6Rgn0WPABaIj7e5xINQOtmPWU2VPpBlSVe9V0RIaem8oa5J918O65yYTzBe03c_sMVBcc8j9Ef9IyDVLacy3BqKnSjOqMaeRQpB78IEvHQOy-Yxce56PeD8QzLiN8uG3Lu2ygg8IS5-cb4bykw_Zh8CDv-fNVmw",
    "userId": "cTfPMH45wIYJqLLZpMtxNUliFmX2"
}
#### Notes:
You get necessary information for doing requests at "/smi" (see below).
The three main variables needed are "userId", "apikey" and "token". The "apikey" variable renews itself every time you log in into the application for security reasons. Keep these in mind when testing the application because token expires too after on hour.
The posted JSON object should be included in the body of the request as JSON format.

### @myapi.post("/signup")
This is another POST endpoint for signing up into the application.
#### Example Request:
POST http://localhost:5000/signup
Body:
{
    "name": "new",
    "lastName": "new",
    "email": "new6@new6.com",
    "password": "123456"
}
#### Example Response:
Body:
{
    "createdUser": true,
    "email": "new6@new6.com",
    "lastName": "new6",
    "message": "User created succesfully.",
    "name": "new6"
}
#### Notes:
I didn't find necessary to expose any other information after logging in.

### @myapi.post("/smi")
This endpoint is the integration with the Alpha Vantage information. Here the application checks that the provided apikey match with the apikey allocated in the database. Each user has his own encrypted apikey.
As regard as the Alpha Vantage API key, is allocated in the .env.example file (remember creating your own before running the application).
Once you run the application, a FERNET_KEY variable is aggregated to the .env file in order to encrypt and decrypt the user's API keys.
#### Example Request:
POST http://localhost:5000/smi?symbol=AAPL
Header:
userId = cTfPMH45wIYJqLLZpMtxNUliFmX2
apikey = gAAAAABhGyfo19Tdf5H2SqnsyF3XPRH1sf3ZaBnZ2srolXeWw25lvdjQPOtAU99SG6fQmECZmLjHMM7YhSJ6sWiEtHXpBcPtBozKa80MUs0WTm-HXtrIVRo=
token = eyJhbGciOiJSUzI1NiIsImtpZCI6IjM2NGU4NTQ1NzI5OWQ5NzIxYjczNDQyZGNiNTQ3Y2U2ZDk4NGRmNTkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc3RvY2stbWFya2V0LWFwaS1zZXJ2aWNlIiwiYXVkIjoic3RvY2stbWFya2V0LWFwaS1zZXJ2aWNlIiwiYXV0aF90aW1lIjoxNjI5MTY5NjQwLCJ1c2VyX2lkIjoiY1RmUE1INDV3SVlKcUxMWnBNdHhOVWxpRm1YMiIsInN1YiI6ImNUZlBNSDQ1d0lZSnFMTFpwTXR4TlVsaUZtWDIiLCJpYXQiOjE2MjkxNjk2NDAsImV4cCI6MTYyOTE3MzI0MCwiZW1haWwiOiJuZXc1QG5ldzUuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm5ldzVAbmV3NS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.Ym2KDfe9By_HMvoXIsyrbJ_I3A9peNXOVvh-QJXFOWGDtzNYYPpNstShFmWYnSTpP1r3nnXXo23EH1FIu-wMeMFYrG1BfrKQYPdDsdLXzCCOZKl_Mu5ApWLWXEwoP9Mo-PmTzM7CHQ6A4UkPIE06VguKPBsryT2K-BGjyNHxXkZmcdIdeCzWidU6Rgn0WPABaIj7e5xINQOtmPWU2VPpBlSVe9V0RIaem8oa5J918O65yYTzBe03c_sMVBcc8j9Ef9IyDVLacy3BqKnSjOqMaeRQpB78IEvHQOy-Yxce56PeD8QzLiN8uG3Lu2ygg8IS5-cb4bykw_Zh8CDv-fNVmw
#### Example Response:
Body:
{
    "Last Closings": [
        {
            "close": 151.12,
            "date": "2021-08-16",
            "high": 151.19,
            "low": 146.47,
            "open": 148.535
        },
        {
            "close": 149.1,
            "date": "2021-08-13",
            "high": 149.4444,
            "low": 148.27,
            "open": 148.97
        }
    ],
    "Meta Data": {
        "1. Information": "Daily Prices (open, high, low, close) and Volumes",
        "2. Symbol": "AAPL",
        "3. Last Refreshed": "2021-08-16",
        "4. Output Size": "Compact",
        "5. Time Zone": "US/Eastern"
    },
    "Results": {
        "high": 151.19,
        "low": 146.47,
        "open": 148.535,
        "variation": 2.02
    }
}
#### Notes:
Remember to take note about those three variables (apikey, userId, token), before testing this endpoint. Note that the "symbol" is allocated in the query string, because I believe that makes the URI more readeble, and let the header data for security purposes only.

### @myapi.post("/log")
Since the alpha tester don't have access to the Firebase Real Time Database, I've created another endpoint for consulting log entries. As you can see below is a simple GET request giving the tester the possibility of reading the saved data after each user request.
I didn't invest to much time with the access rules for this database in search of achieving the API throttling issue and other issues.
#### Example Request:
GET http://localhost:5000/log?userId=cTfPMH45wIYJqLLZpMtxNUliFmX2
#### Example Response:
Body:
{
    "-MhH4GEkyjrYm4PKhkm2": {
        "email": "new5@new5.com",
        "endpoint": "/smi",
        "method": "GET",
        "symbol": "AMZN",
        "timestamp": 1629169718256
    },
    "-MhH4Hi7SuKJZLc7Gcf5": {
        "email": "new5@new5.com",
        "endpoint": "/smi",
        "method": "GET",
        "symbol": "AMZN",
        "timestamp": 1629169724297
    },
    "-MhH4JUmguFavYf4Baqq": {
        "email": "new5@new5.com",
        "endpoint": "/smi",
        "method": "GET",
        "symbol": "AAPL",
        "timestamp": 1629169731570
    }
}
#### Notes:
As you can see is just a simple log information that could be improved, saving the information getted at the request time, for example.

### API Throttling
In order to achive this issue I've used Flask-Limiter package, and find it very simple to implement because of the use of decorators for each endpoint. I've leaved a global configuration commented for future modifications.

### Error Handling
This is the weakest point of the application because I've focused in developing a fully functional application first, as I always do. But you can see that in each response, I've leaved a subcode for redacting the proper messages in future releases. For example:
Body:
{
    "action": "/login",
    "message": "The request method is not supported by the server and cannot be handled.",
    "status": 501,
    "sub_code": 6
}
Look at the variable sub_code when testing the application, and you will notice that is not always the same for different errors. This was just a matter of time.

### Data Validation
Another weak point of the application. I didn't have enough time for redacting the database rules (at Firebase) in order to do a proper data validation. This is the preferred way to do it as I'm concerned. Of course you can add Python validations, but this is a additional security functionality in addition to Real Time Database rules, that works perfectly.

### Comming soon
Implement the proper responses for all these test cases:

1. User already exists in the datase.
  You can't sign up the same user twice, but you don't get the proper message yet.
2. Password is too weak. 
  Firebase has a simple validation for passwords, it can be improved using rules and regex.
4. User data is not valid. 
  For example now you can save an empty name or last name.
5. Incorrect password during log in.
  You can't log in into the application with an incorrect password, but you don't get the proper message either.
6. Redact proper messages for each error sub_code.
7. Add a timestamp field for the user's data.
8. Rename some files for better fuctionality understanding.
9. Improving never ends, but these are the primary points I've noticed during development.

### Conclusion
It was a really challeging project because I have the opportunity to mix many technologies I've learned recently, and also have to invest some time to achieve issues I've never faced.
I know that is not a complete application, there are a lot of things to improve. I've tried to maintain the code clean. Sometimes I've had to search for another way of solving the same issue too.
Thanks for the opportunity you have gave me. I've felt really committed with the task.
Any suggestions are welcome.

