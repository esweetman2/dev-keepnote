from Helpers.Firebase_Auth import __firebase_config__
from firebase_admin import auth
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
FB_AUTH_KEY = os.getenv("FB_AUTH_KEY")


def signInUser(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FB_AUTH_KEY}"
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": True
    })
    try:
        res = requests.post(url=url, data=payload)
    except:
        return json.dumps({"message": "Something went wrong"})
    else:
        response = res.json()
        return response


user = signInUser("test@test.com", "password")
print("HERE", user)

    


