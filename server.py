from flask_cors import CORS
from app import create_app
from app.config.db_connection import connectToMySQL
import os

app = create_app()

CORS(app, resources={r"/*": {"origins": os.getenv('ORIGIN')}}, supports_credentials=True)

from app.controllers.users import user_bp
from app.controllers.vouchers import voucher_bp
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(voucher_bp, url_prefix='/voucher')

app.run(debug=True)

try:
    connectToMySQL().query_db("SELECT 1")
    print("✅ Conectado a MySQL")
except:
    print("❌ Error MySQL")
