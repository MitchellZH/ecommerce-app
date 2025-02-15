from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import db, User, bcrypt
import json

auth_routes = Blueprint("auth", __name__)


# REGISTER USER
@auth_routes.route("/register", methods=["POST"])
def register():
    data = request.json
    if db.users.find_one({"email": data["email"]}):
        return jsonify({"message": "User already exists"}), 400

    new_user = User(data["username"], data["email"], data["password"])
    db.users.insert_one(new_user.to_dict())

    return jsonify({"message": "User registered successfully"}), 201


@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.json
    user = db.users.find_one({"email": data["email"]})
    
    if user and bcrypt.check_password_hash(user["password"], data["password"]):
        identity = json.dumps(
            {
                "username": user["username"],
                "email": user["email"],
                "is_admin": user.get("is_admin", False),  # Default to False
            }
        )
        access_token = create_access_token(identity=identity)

        return jsonify({"access_token": access_token}), 200

    return jsonify({"message": "Invalid credentials"}), 401
