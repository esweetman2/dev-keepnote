from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, abort, reqparse
# from flask_marshmallow import Marshmallow
from Resources.resources import *
from flask_cors import CORS
from Helpers.Firebase_Auth import verifyUser
from Models.models import *
from dotenv import load_dotenv
import json
import os

class AppUserRoute(Resource):
    @marshal_with(resource_fields)
    def get(self):
        if request.headers["Authorization"]:
            access_key = request.headers["Authorization"]
            # print(access_key)
            decoded = verifyUser(access_key)
            if type(decoded) is dict:
                # decoded['uid']
                user = Users.query.filter_by(user_uuid=decoded['uid']).first()
                if user:
                    return user
                else:

                    return abort(400)
            elif type(decoded) is str:

                # return json.loads(decoded)
                return abort(400, error="BAD REQUEST")
        else:
            return abort(400)

    @marshal_with(resource_fields)
    def put(self):
        data = request.get_json()
        # for item in data:
        #     print(item, data[item])
        #     print("Make edit on")
        # uuid = data['uuid']
        # user = Users.query.filter_by(uuid = uuid).first()
        # user.first_name = "Joe"
        # db.session.commit()
        # print(user)
        return "user"

    def post(self):
        if request.headers['Content-Type'] == "application/json" and request.headers['authorization']:
            data = request.get_json()
            try:
                email = data['email']
                uid = data['uid']
            except:
                return abort(404)
            access_key = request.headers['authorization']

            decoded = verifyUser(access_key)
            if type(decoded) is dict:
                # print(decoded)
                decoded_uid = decoded['user_id']
                decoded_email = email
                if decoded_uid == uid and email == decoded_email:
                    try:
                        new_user = Users(
                            user_uuid=decoded['uid'],
                            email=email
                        )
                        db.session.add(new_user)
                        db.session.commit()
                        return {"message": "User added!"}
                    except:
                        return {"message": "ERROR"}
                else:
                    return abort(400, error="Wrong User")
            else:
                return abort(400, error="BAD REQUEST")
        else:
            return abort(400, error="BAD REQUEST")

