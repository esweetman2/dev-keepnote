from Helpers.Firebase_Auth import __firebase_config__ 
from firebase_admin import auth
# import requests
import json
from dotenv import load_dotenv
# import os

# load_dotenv()
# FB_AUTH_KEY = os.getenv("FB_AUTH_KEY")

def verifyUser(key):
    # print(auth_token)
    if key.startswith("Bearer"):
        token = key[7:]
        try:
            decoded_token = auth.verify_id_token(token)
        except auth.ExpiredIdTokenError as e:
            return json.dumps({"message": "Token has Expired"})
        except:
            return json.dumps({"message": "Something else went wrong"})
        else:
            return decoded_token
    else:
        return False
