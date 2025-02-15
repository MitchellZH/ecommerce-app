import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()  # Load environment variables from .env


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is missing from environment variables!")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY is missing from environment variables!")
    # Set JWT expiration time (adjust as needed)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    MONGO_URI = os.environ.get("MONGO_URI")
    if not MONGO_URI:
        raise ValueError("MONGO_URI is missing from environment variables!")
