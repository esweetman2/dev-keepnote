# from ast import Delete
# from cmath import e
# from logging import NOTSET
from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, abort
# from flask_marshmallow import Marshmallow 
from Resources.resources import *
from flask_cors import CORS
from Models.models import *
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
class TestGet(Resource):
    def get(self):
        return {"message": "working"}
## Application User
class AppUserRoute(Resource):

    @marshal_with(resource_fields)
    def get(self):
        if request.headers['Content-Type'] == "application/json":
            data = request.get_json()
            user = Users.query.filter_by(user_uuid=data['uuid']).first()
            if user:
                return user
            else:
                abort(400)
        else:
            abort(400)

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
        if request.headers['Content-Type'] == "application/json":
            data = request.get_json()
            # print(data["uuid"])
            try:
                new_user = Users(
                    uuid = data["uuid"],
                    first_name = data["first_name"], 
                    last_name=data["last_name"], 
                    email = data["email"]
                    )
                db.session.add(new_user)
                db.session.commit()
                return {"message": "User added!"}
            except:
                return {"message": "ERROR"}
        else:
            return {"message": "Something went wrong"}

## Adding a Client
class ClientRoute(Resource):
    @marshal_with(get_clients_resource_fields)
    def get(self):
        if request.headers['Content-Type'] == "application/json":
            data = request.get_json()
            # print(data)
            uuid = data['uuid']
            clients = Clients.query.filter_by(user_uuid=uuid).all()
            return clients
        else:
            abort(400)


    def post(self):
        if request.headers['Content-Type'] == "application/json":
            data = request.get_json()
            # print(data)
            # try:
            new_client = Clients(
                user_uuid = data["uuid"],
                client_name = data["client_name"], 
                client_phone=data["client_phone"], 
                client_address = data["client_address"]
                )
            db.session.add(new_client)
            db.session.commit()
                # return {"message": "Client added!"}
            # except:
            return {"message": "ERROR"}
        else:
            return {"message": "Something went wrong"}
    



## Notes Route
class NotesRoute(Resource):
    @marshal_with(get_notes_resource_fields)
    def get(self):
        if request.headers['Content-Type'] == "application/json":
            data = request.get_json()
            # print(data)
            uuid = data['uuid']
            notes = ClientNotes.query.filter_by(user_uuid=uuid).all()
            return notes
        else:
            abort(400)

    def post(self):
        if request.headers['Content-Type'] == "application/json":
            data = request.get_json()
            # print(data)
            try:
                new_note = ClientNotes(
                    user_uuid = data["uuid"], 
                    client_id = data["client_id"], 
                    notes = data["notes"]
                    )
                db.session.add(new_note)
                db.session.commit()
                return {"message": "Note added!"}
            except:
                return {"message": "ERROR"}
        else:
            return {"message": "Something went wrong"}


## Adding a product
class ProductRoute(Resource):

    @marshal_with(get_products_resource_fields)
    def get(self):
        if request.headers['Content-Type'] == "application/json":
        # print(uuid)
            data = request.get_json()
            uuid = data['uuid']
            products = Products.query.filter_by(user_uuid = uuid).all()
            return products
        else:
            abort(400)

    def post(self):
        if request.headers['Content-Type'] == "application/json":
            data = request.get_json()
            # print(data)
            try:
                new_product = Products(
                    user_uuid = data["uuid"], 
                    product_name = data["product_name"], 
                    product_price = data["product_price"]
                    )

                db.session.add(new_product)
                db.session.commit()
                return {"message": "Product added!"}
            except:
                return {"message": "ERROR"}
        else:
            return {"message": "Something went wrong"}


    # @marshal_with(get_products_resource_fields)
    def delete(self):
        if request.headers['Content-Type'] == "application/json":

            data = request.get_json()
            uuid = data['uuid']
            product_id = data['id']

            try:
                delete_product = Products.query.filter_by(id = product_id).first()
                if delete_product.user_uuid != uuid:
                    return {"message": "QUERY ERROR"}
                else:
                    db.session.delete(delete_product)
                    db.session.commit()

                    return {"message": f"Product {delete_product.product_name} has been deleted"}
            except:
                return {"message": "Could not delete"}
        else:
            return {"message": "Something went wrong"}

## Adding a Appointment
class AppointmentRoute(Resource):
    @marshal_with(get_appointments_resource_fields)
    def get(self):
        if request.headers['Content-Type'] == "application/json":
            data = request.get_json()
            # print(data)
            uuid = data['uuid']
            appointments = Appointments.query.filter_by(user_uuid=uuid).all()
            return appointments
        else:
            abort(400)
    
    
    def post(self):
        if request.headers['Content-Type'] == "application/json":
            data = request.get_json()
            # print(data['appointment_date'])
            try:
                new_appointment = Appointments(
                    user_uuid = data["uuid"], 
                    appointment_client_id = data["appointment_client_id"],
                    appointment_date = data["appointment_date"],
                    appointment_location = data["appointment_location"], 
                    appointment_client_name = data['appointment_client_name'],
                    appointment_title = data['appointment_title']
                    )

                db.session.add(new_appointment)
                db.session.commit()
                return {"message": "Appointment added!"}
            except:
                return {"message": "ERROR"}
        else:
            return {"message": "Something went wrong"}
    
    def delete(self):
        if request.headers['Content-Type'] == "application/json":
            
            data = request.get_json()
            uuid = data['uuid']
            appointment_id = data['id']

            try:
                delete_appointment = Appointments.query.filter_by(id = appointment_id).first()
                if delete_appointment.user_uuid != uuid:
                    return {"message": "QUERY ERROR"}
                else:
                    db.session.delete(delete_appointment)
                    db.session.commit()

                    return {"message": f"Appointment at {delete_appointment.appointment_location} has been deleted"}
            except:
                return {"message": "Could not delete"}
        else:
            return {"message": "Something went wrong"}

api.add_resource(TestGet, f"/{api_endpoint}/test")
api.add_resource(AppUserRoute, f"/{api_endpoint}/user")
api.add_resource(ClientRoute, f"/{api_endpoint}/client")
api.add_resource(NotesRoute, f"/{api_endpoint}/note")
api.add_resource(ProductRoute, f"/{api_endpoint}/product")
api.add_resource(AppointmentRoute, f"/{api_endpoint}/appointment")



if __name__ == '__main__':
    app.run(debug=True)