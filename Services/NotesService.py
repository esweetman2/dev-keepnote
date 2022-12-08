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


class NotesRoute(Resource):
    
    @marshal_with(get_notes_resource_fields)
    def get(self):
        if request.headers['Content-Type'] == "application/json" and request.headers["authorization"]:
            decoded_token = verifyUser.verifyUser(request.headers["Authorization"])
            data = request.get_json()
            if type(decoded_token) is dict and decoded_token['user_id'] == data['uid']:
                decoded_uid = decoded_token['user_id']
                notes = ClientNotes.query.filter_by(user_uuid=decoded_uid).all()
                return notes
            elif type(decoded_token) is str:
                return abort(400, error=json.loads(decoded_token))
            else:
                return abort(400, error="Token Error")
        else:
            abort(400, error="BAD REQUEST")

    def post(self):
        if request.headers['Content-Type'] == "application/json" and request.headers["authorization"]:
            decoded_token = verifyUser.verifyUser(request.headers["Authorization"])
            data = request.get_json()
            if type(decoded_token) is dict and decoded_token['user_id'] == data['uid']:
                try:
                    new_note = ClientNotes(
                        user_uuid=data["uid"],
                        client_id=data["client_id"],
                        notes=data["notes"]
                    )
                    db.session.add(new_note)
                    db.session.commit()
                    return {"message": "Note added!"}
                except:
                    return {"message": "ERROR"}
            elif type(decoded_token) is str:
                return abort(400, error=json.loads(decoded_token))
            else:
                return abort(400, error="Token Error")
        else:
            return abort(400, error="BAD REQUEST")