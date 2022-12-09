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



# Adding a Client
class ClientsRoute(Resource):
    @marshal_with(get_clients_resource_fields)
    def get(self):
        if request.headers['Content-Type'] == "application/json" and request.headers["authorization"]:
            # data = request.get_json()
            # print(data)
            decoded_token = verifyUser.verifyUser(request.headers["Authorization"])
            # print(decoded_token)
            # and decoded_token['user_id'] == data['uuid']
            if type(decoded_token) is dict:
                # print(decoded_token)
                uid = decoded_token['user_id']
                clients = Clients.query.filter_by(user_uuid=uid).all()
                # print(clients)
                return clients
            elif type(decoded_token) is str:
                print("HERE", json.loads(decoded_token))
                return abort(400, error=json.loads(decoded_token))
            else:
                return abort(400, error="BAD REQUEST")
        else:
            abort(400)

    @marshal_with(get_clients_resource_fields)
    def post(self):
        if request.headers['Content-Type'] == "application/json" and request.headers["Authorization"]:
            data = request.get_json()
            # print(data)
            if "uid" not in data: return abort(400, error="Your request is missing something")
            decoded_token = verifyUser.verifyUser(request.headers["Authorization"])
            if type(decoded_token) is dict and data['client_name'] and decoded_token['user_id'] == data['uid']:
                # print(decoded_token)
                try:
                    new_client = Clients(
                        user_uuid=decoded_token['uid'],
                        client_name=data["client_name"],
                    )
                    db.session.add(new_client)
                    db.session.commit()
                    return new_client
                except Exception as e:
                    print(e)
                    return f"error: Counldn't add to DB"
            elif type(decoded_token) is str:
                return abort(400, decoded_token)
            else:
                return abort(400, error="BAD REQUEST no news")
        else:
            return abort(400, error="BAD REQUEST")


### INDIVIDUAL CLIENT ####

class Client(Resource):
    @marshal_with(get_clients_resource_fields)
    def get(self, id):
        if request.headers['Content-Type'] == "application/json" and request.headers["authorization"]:

            decoded_token = verifyUser.verifyUser(request.headers["Authorization"])
            data = request.get_json()
            if "uid" not in data: return abort(400, error="Your request is missing something")

            if type(decoded_token) is dict and decoded_token['user_id'] == data['uid']:

                client = Clients.query.filter_by(user_uuid=data['uid'], id=id).first()
                return client
            elif type(decoded_token) is str:
                return abort(400, error=json.loads(decoded_token))
            else:
                return abort(400, error="Token Error")
        else:
            abort(400, error="BAD REQUEST")

    @marshal_with(get_clients_resource_fields)
    def put(self, id):
        
        if request.headers['Content-Type'] == "application/json" and request.headers["Authorization"]:
            data = request.get_json()
            if "uid" not in data: return abort(400, error="Your request is missing something")
            decoded_token = verifyUser.verifyUser(request.headers["Authorization"])
            # print(decoded_token)

            if type(decoded_token) is dict and data['update_name'] and decoded_token['user_id'] == data['uid']:
                
                try:
                    updated_client = Clients.query.filter_by(user_uuid=data['uid'], id=id).first()
                    updated_client.client_name = data['update_name']
                    db.session.commit()
                    return updated_client
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
        # print(id)
        if request.headers['Content-Type'] == "application/json" and request.headers["Authorization"]:
            data = request.get_json()
            if "uid" not in data: return abort(400, error="Your request is missing something")
            # print("HERE", data)
            decoded_token = verifyUser.verifyUser(request.headers["Authorization"])
            # print(decoded_token)

            if type(decoded_token) is dict and decoded_token['user_id'] == data['uid']:
                
                try:
                    updated_client = Clients.query.filter_by(user_uuid=data['uid'], id=id)
                    updated_client.delete()
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