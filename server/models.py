from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from config import Config
from marshmallow import Schema, fields, ValidationError

bcrypt = Bcrypt()

client = MongoClient(Config.MONGO_URI)

# Connect to MongoDB
db = (
    client.get_database()
)

class User:
    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        self.is_admin = is_admin

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "is_admin": self.is_admin,
        }


class UserSchema(Schema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(
        required=True, load_only=True
    )  # Hide password from response
    is_admin = fields.Boolean(default=False)


class Product:
    def __init__(self, name, price, description, image, stock):
        self.name = name
        self.price = price
        self.description = description
        self.image = image
        self.stock = stock

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "image": self.image,
            "stock": self.stock,
        }


class ProductSchema(Schema):
    name = fields.String(required=True)
    price = fields.Float(required=True)
    description = fields.String(required=True)
    image = fields.String(required=True)
    stock = fields.Integer(required=True, validate=lambda x: x >= 0)