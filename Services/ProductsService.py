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