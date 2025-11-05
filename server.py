from flask_cors import CORS
from app import app
from app.config.db_connection import connectToMySQL
import os

def create_app():
    CORS(app, resources={r"/*": {"origins": os.getenv('ORIGIN')}}, supports_credentials=True) 

    from app.controllers.users import user_bp
    from app.controllers.vouchers import voucher_bp
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(voucher_bp, url_prefix='/voucher')

create_app()

print("✅ Conectado a MySQL") if connectToMySQL().query_db("SELECT 1") else print("❌ Error MySQL")


if __name__ == '__main__':
    app.run(debug=True)