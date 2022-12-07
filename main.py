from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, abort, reqparse
# from flask_marshmallow import Marshmallow
from Resources.resources import *
from flask_cors import CORS
from src.Services.loginService import *
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

# Application User


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


# Adding a Client
class ClientsRoute(Resource):
    @marshal_with(get_clients_resource_fields)
    def get(self):
        if request.headers['Content-Type'] == "application/json" and request.headers["authorization"]:
            # data = request.get_json()
            # print(data)
            decoded_token = verifyUser(request.headers["Authorization"])
            # print(decoded_token)
            # and decoded_token['user_id'] == data['uuid']
            if type(decoded_token) is dict:
                # print(decoded_token)
                uuid = decoded_token['user_id']
                clients = Clients.query.filter_by(user_uuid=uuid).all()
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
            decoded_token = verifyUser(request.headers["Authorization"])
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
                    # return {
                    #     "success": True,
                    #     "message":f"Client added {new_client.client_name}"
                    #     }
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
# client_put_args = reqparse.RequestParser()
# client_put_args.add_argument("id", type=int, help="Need an ID")

class Client(Resource):
    @marshal_with(get_clients_resource_fields)
    def put(self, id):

        if request.headers['Content-Type'] == "application/json" and request.headers["Authorization"]:
            data = request.get_json()
            decoded_token = verifyUser(request.headers["Authorization"])
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
        print(id)
        if request.headers['Content-Type'] == "application/json" and request.headers["Authorization"]:
            data = request.get_json()
            decoded_token = verifyUser(request.headers["Authorization"])
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


# Notes Route
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
                    user_uuid=data["uuid"],
                    client_id=data["client_id"],
                    notes=data["notes"]
                )
                db.session.add(new_note)
                db.session.commit()
                return {"message": "Note added!"}
            except:
                return {"message": "ERROR"}
        else:
            return {"message": "Something went wrong"}


# Adding a product
class ProductRoute(Resource):

    @marshal_with(get_products_resource_fields)
    def get(self):
        if request.headers['Content-Type'] == "application/json":
            # print(uuid)
            data = request.get_json()
            uuid = data['uuid']
            products = Products.query.filter_by(user_uuid=uuid).all()
            return products
        else:
            abort(400)

    def post(self):
        if request.headers['Content-Type'] == "application/json":
            data = request.get_json()
            # print(data)
            try:
                new_product = Products(
                    user_uuid=data["uuid"],
                    product_name=data["product_name"],
                    product_price=data["product_price"]
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
                delete_product = Products.query.filter_by(
                    id=product_id).first()
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

# Adding a Appointment


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
                    user_uuid=data["uuid"],
                    appointment_client_id=data["appointment_client_id"],
                    appointment_date=data["appointment_date"],
                    appointment_location=data["appointment_location"],
                    appointment_client_name=data['appointment_client_name'],
                    appointment_title=data['appointment_title']
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
                delete_appointment = Appointments.query.filter_by(
                    id=appointment_id).first()
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


api.add_resource(AppUserRoute, f"/{api_endpoint}/user")

api.add_resource(ClientsRoute, f"/{api_endpoint}/clients")
api.add_resource(Client, f"/{api_endpoint}/client/<int:id>")

api.add_resource(NotesRoute, f"/{api_endpoint}/note")

api.add_resource(ProductRoute, f"/{api_endpoint}/product")

api.add_resource(AppointmentRoute, f"/{api_endpoint}/appointment")

# api.add_resource(SignInUser, f"/{api_endpoint}/login")
# api.add_resource(CreateUser, f"/{api_endpoint}/register")


if __name__ == '__main__':
    app.run(debug=True, host="192.168.1.165", port="5000")
    # app.run(ssl_context='adhoc', debug=True, host="192.168.1.165", port="5000")
    # app.run(host="192.168.1.165", port="19000", debug=True)
