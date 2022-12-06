from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


db = SQLAlchemy()

# Parent
class Users(db.Model):
    __tablename__= 'users'
    user_uuid = db.Column(db.String(255), primary_key=True, nullable=False, unique=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=False)
    register_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_paid = db.Column(db.Boolean, default=False, nullable=False)
    clients = db.relationship("Clients", backref='users')

# Child
class Clients(db.Model):
    __tablename__= 'clients'
    id = db.Column(db.Integer, primary_key=True) 
    user_uuid = db.Column(db.String(255), db.ForeignKey("users.user_uuid"), nullable=False)
    client_name = db.Column(db.String(255), nullable=False)
    client_phone = db.Column(db.String(255))
    client_address = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    client_notes = db.relationship("ClientNotes", backref="clients")
    client_appointments = db.relationship("Appointments", backref='clients')

# Child
class ClientNotes(db.Model):
    __tablename__= 'clientnotes'
    id = db.Column(db.Integer, primary_key=True) 
    user_uuid = db.Column(db.String(255), db.ForeignKey("users.user_uuid"), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    notes = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Child
class Products(db.Model):
    __tablename__= 'products'
    id = db.Column(db.Integer, primary_key=True) 
    user_uuid = db.Column(db.String(255), db.ForeignKey("users.user_uuid"), nullable=False)
    product_name = db.Column(db.String(100), unique=True)
    product_price = db.Column(db.Float)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Child
class Appointments(db.Model):
    __tablename__= 'appointments'
    id = db.Column(db.Integer, primary_key=True) 
    user_uuid = db.Column(db.String(255), db.ForeignKey("users.user_uuid"), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    appointment_location = db.Column(db.String(1000))
    appointment_client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    appointment_client_name = db.Column(db.String(255))
    appointment_title = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
