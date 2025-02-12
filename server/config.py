import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is missing from environment variables!")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY is missing from environment variables!")
    MONGO_URI = os.environ.get("MONGO_URI")
    if not SECRET_KEY:
        raise ValueError("MONGO_URI is missing from environment variables!")
