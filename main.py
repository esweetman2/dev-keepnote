from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, abort, reqparse
# from flask_marshmallow import Marshmallow
from Resources.resources import *
from flask_cors import CORS
from Helpers.Firebase_Auth import verifyUser
from Models.models import *
from Services.ClientService import *
from Services.NotesService import *
from Services.AppUserService import *
from Services.ProductsService import *
from Services.AppointmentsService import *
import json
from dotenv import load_dotenv
import os


load_dotenv()
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SERVER = os.getenv("DB_SERVER")
DB_PORT = os.getenv("DB_PORT")
DB_DATABASE = os.getenv("DB_DATABASE")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_DATABASE}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

api_endpoint = "api/v1"
CORS(app)

api = Api(app)

api.add_resource(AppUserRoute, f"/{api_endpoint}/user")

api.add_resource(ClientsRoute, f"/{api_endpoint}/clients")
api.add_resource(Client, f"/{api_endpoint}/client/<int:id>")

api.add_resource(NotesRoute, f"/{api_endpoint}/notes")
api.add_resource(SingleNoteRoute, f"/{api_endpoint}/note/<int:id>")

api.add_resource(ProductRoute, f"/{api_endpoint}/product")

api.add_resource(AppointmentRoute, f"/{api_endpoint}/appointment")

# api.add_resource(SignInUser, f"/{api_endpoint}/login")
# api.add_resource(CreateUser, f"/{api_endpoint}/register")


if __name__ == '__main__':
    app.run(debug=True, host="192.168.1.165", port="5000")
    # app.run(ssl_context='adhoc', debug=True, host="192.168.1.165", port="5000")
    # app.run(host="192.168.1.165", port="19000", debug=True)
