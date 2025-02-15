from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from routes.auth_routes import auth_routes
from routes.product_routes import product_routes

# Initialize Flask app
app = Flask(__name__)

# Load configuration from config.py
app.config["SECRET_KEY"] = Config.SECRET_KEY
app.config["JWT_ALGORITHM"] = "HS256"
app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = Config.JWT_ACCESS_TOKEN_EXPIRES

# Enable CORS (for frontend to access API)
CORS(app)

# Initialize JWT manager
jwt = JWTManager(app)

# Register blueprints (modular routes)
app.register_blueprint(auth_routes, url_prefix="/api/auth")
app.register_blueprint(product_routes, url_prefix="/api/products")

# Root route to test API is running
@app.route("/")
def home():
    return {"message": "E-commerce API is running successfully!"}


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
