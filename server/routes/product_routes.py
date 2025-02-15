from flask import Blueprint, request, jsonify
from models import db, Product, ProductSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
import json
from bson.objectid import ObjectId

product_routes = Blueprint("products", __name__)
product_schema = ProductSchema() # Create schema instance for validation


# GET ALL PRODUCTS
@product_routes.route("/", methods=["GET"])
def get_products():
    products = list(
        db.products.find({}, {"_id": 0})
    )
    return jsonify(products), 200


# Helper function to check admin rights
def admin_required():
    current_user = json.loads(get_jwt_identity())
    if not current_user.get("is_admin", False):
        return jsonify({"message": "Access denied. Admins only."}), 403
    return None, None


# ADD NEW PRODUCT (Admin Only)
@product_routes.route("/", methods=["POST"])
@jwt_required()
def add_product():
    # Verify user has the admin role
    error_resp, error_code = admin_required()
    if error_resp:
        return error_resp, error_code

    # Validate request data
    try:
        validated_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # Create and insert new product
    new_product = Product(**validated_data)
    db.products.insert_one(new_product.to_dict())

    return jsonify({"message": "Product added successfully!"}), 201


# DELETE PRODUCT (Admin Only)
@product_routes.route("/<string:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id):
    # Verify admin
    error_resp, error_code = admin_required()
    if error_resp:
        return error_resp, error_code

    # Delete the product using its ObjectId
    try:
        result = db.products.delete_one({"_id": ObjectId(product_id)})
    except Exception as e:
        return jsonify({"message": "Invalid product id", "error": str(e)}), 400

    if result.deleted_count > 0:
        return jsonify({"message": "Product deleted successfully!"}), 200
    return jsonify({"message": "Product not found."}), 404


# UPDATE PRODUCT (Admin Only)
@product_routes.route("/<string:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id):
    # Verify admin
    error_resp, error_code = admin_required()
    if error_resp:
        return error_resp, error_code

    # Validate request data for update
    try:
        validated_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # Update product using its ObjectId
    try:
        result = db.products.update_one(
            {"_id": ObjectId(product_id)}, {"$set": validated_data}
        )
    except Exception as e:
        return jsonify({"message": "Invalid product id", "error": str(e)}), 400

    if result.modified_count > 0:
        return jsonify({"message": "Product updated successfully!"}), 200
    return jsonify({"message": "Product not found or data is the same."}), 404
