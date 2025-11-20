from flask import Flask;
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__);
    app.secret_key = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_KEY')
    # Inicializar extensiones con la app
    bcrypt.init_app = Bcrypt(app)
    jwt.init_app = JWTManager(app)
    return app