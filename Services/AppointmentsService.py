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