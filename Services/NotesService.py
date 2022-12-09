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
            if "uid" not in data: return abort(400, error="Your request is missing something")
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
            # print(decoded_token)
            data = request.get_json()
            if "uid" not in data: return abort(400, error="Your request is missing something")
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

class SingleNoteRoute(Resource):
    @marshal_with(get_notes_resource_fields)
    def get(self, id):
        if request.headers['Content-Type'] == "application/json" and request.headers["authorization"]:
            decoded_token = verifyUser.verifyUser(request.headers["Authorization"])
            data = request.get_json()
            if "uid" not in data: return abort(400, error="Your request is missing something")

            if type(decoded_token) is dict and decoded_token['user_id'] == data['uid']:
                decoded_uid = decoded_token['user_id']
                note = ClientNotes.query.filter_by(user_uuid=data['uid'], id=id).first()
                return note
            elif type(decoded_token) is str:
                return abort(400, error=json.loads(decoded_token))
            else:
                return abort(400, error="Token Error")
        else:
            abort(400, error="BAD REQUEST")

    @marshal_with(get_notes_resource_fields)
    def put(self, id):
        if request.headers['Content-Type'] == "application/json" and request.headers["Authorization"]:
            data = request.get_json()
            decoded_token = verifyUser.verifyUser(request.headers["Authorization"])
            # print(decoded_token)
            if "updated_note" not in data: return abort(400, error="Your request is missing something")
            if "uid" not in data: return abort(400, error="Your request is missing something")

            if type(decoded_token) is dict and decoded_token['user_id'] == data['uid']:
                
                try:
                    updated_note = ClientNotes.query.filter_by(user_uuid=data['uid'], id=id).first()
                    updated_note.notes = data['updated_note']
                    db.session.commit()
                    return updated_note
                except Exception as e:
                    # print(e)
                    return f"error: Counldn't add to DB"

            elif type(decoded_token) is str:
                return abort(400, error=decoded_token)

            else:
                return abort(400, error="BAD REQUEST no news")
        else:
            # print("abort")
            return abort(400)
    def delete(self, id):
        if request.headers['Content-Type'] == "application/json" and request.headers["Authorization"]:

            data = request.get_json()
            if "uid" not in data: return abort(400, error="Your request is missing something")

            decoded_token = verifyUser.verifyUser(request.headers["Authorization"])
        
            if type(decoded_token) is dict and decoded_token['user_id'] == data['uid']:
                try:
                    deleted_client = ClientNotes.query.filter_by(user_uuid=data['uid'], id=id)
                    deleted_client.delete()
                    db.session.commit()
                except Exception as e:
                    print(e)
                    return f"error: Counldn't Delete"
            elif type(decoded_token) is str:
                return abort(400, error=decoded_token)
            else:
                return abort(400, error="BAD REQUEST no news")
        else:
            # print("abort")
            return abort(400)
        return {"message": "Deleted"}