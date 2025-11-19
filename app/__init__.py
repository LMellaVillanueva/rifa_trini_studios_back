from flask import Flask;
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os

def create_app():
    app = Flask(__name__);
    app.secret_key = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_KEY')
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)
    return app