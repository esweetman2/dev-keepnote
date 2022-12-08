from Helpers.Firebase_Auth import __firebase_config__ 
from firebase_admin import auth, exceptions
import requests
import json
from dotenv import load_dotenv
# import os

# load_dotenv()
# FB_AUTH_KEY = os.getenv("FB_AUTH_KEY")


def createUser(email,password):
    try:
        user = auth.create_user(email = email,password = password)
        print(user)
    except auth.EmailAlreadyExistsError:
        return json.dumps({"error": "Email already exists"})
    except exceptions.InvalidArgumentError:
        return json.dumps({"error": "Invalid Arguments"})
    except:
        print("LASTLY")
    else:
        print(json.dumps(user.__dict__))
        return json.dumps(user.__dict__)