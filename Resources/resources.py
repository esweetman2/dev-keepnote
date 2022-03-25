from flask_restful import fields

resource_fields = {
    "user_uuid": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String,
    "register_date": fields.DateTime,
    "is_paid": fields.Boolean,
}

get_clients_resource_fields = {
    "id": fields.Integer,
    "user_uuid": fields.String,
    "client_name": fields.String,
    "client_phone": fields.String,
    "client_address": fields.String,
    "created_date": fields.DateTime,
}
get_notes_resource_fields = {
    "id": fields.Integer,
    "user_uuid": fields.String,
    "client_id":fields.Integer,
    "notes": fields.String,
    "created_date": fields.DateTime
}

get_products_resource_fields = {
    "id": fields.Integer,
    "user_uuid": fields.String,
    "product_name": fields.String,
    "product_price": fields.String,
    "created_date": fields.DateTime
}

get_appointments_resource_fields = {
    "id": fields.Integer,
    "user_uuid": fields.String,
    "appointment_date": fields.DateTime,
    "appointment_location": fields.String,
    "appointment_client_id": fields.Integer,
    "appointment_client_name": fields.String,
    "appointment_title": fields.String,
    "created_date": fields.DateTime
}