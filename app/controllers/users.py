from flask import jsonify, request, Blueprint
from app import app
from app.models.User import User
from app.models.Admin import Admin
from app.models.Voucher import Voucher
import uuid
import cloudinary.uploader
from app.config.cloud_config import configure_cloudinary
configure_cloudinary()
from app import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

user_bp = Blueprint('user_bp', __name__)

# Tipos de archivos aceptados
ALLOWED_IMG = {'png','jpg','jpeg','gif','webp'}
ALLOWED_PDF = {'pdf'}

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    data_user = request.form.to_dict()
    voucher = request.files['voucher']
    if not voucher:
        return jsonify({ "error": 'No se envió el comprobante' }), 400

    upload_voucher = cloudinary.uploader.upload(voucher)

    validate_user = User.validate_user(data_user)
    if len(validate_user):
        return jsonify({ "error": validate_user }), 400

    user_existant = User.get_user_by_phone(data_user['phone'])

    if user_existant:
        data_voucher = {
            'image_url': upload_voucher['secure_url'],
            'user_id': user_existant['id'],
            'verified': False,
            'num_of_numbers': int(data_user['num_of_numbers'])
        }
        new_voucher_id = Voucher.insert_voucher(data_voucher)

        if not new_voucher_id:
            return jsonify({ "error": 'Datos incorrectos' }), 400

        user_voucher = Voucher.get_voucher_from_user(user_existant['id'])

        return jsonify({ 
            "user": user_existant['name'], 
            "phone": user_existant['phone'], 
            "email": user_existant['email'],
            "voucher": user_voucher, 
            "existant": 'Al verificar el comprobante se le asignarán números de rifa al mismo usuario.'
            }), 200
    else:
        new_user_id = User.insert_user(data_user)
        if not new_user_id:
            return jsonify({ "error": 'Error en la base de datos' }), 500

        data_voucher = {
            'image_url': upload_voucher['secure_url'],
            'user_id': new_user_id,
            'verified': False,
            'num_of_numbers': int(data_user['num_of_numbers'])
        }
        new_voucher_id = Voucher.insert_voucher(data_voucher)
        if not new_voucher_id:
            return jsonify({ "error": 'Datos incorrectos' }), 400

        get_user = User.get_user_by_id(new_user_id)
        user_voucher = Voucher.get_voucher_from_user(get_user['id'])
            
        return jsonify({ 
            "user": get_user['name'], 
            "phone": get_user['phone'], 
            "email": get_user['email'],
            "voucher": user_voucher,
            }), 200

# Crear un admin MANUALMENTE
@user_bp.route('/admin', methods=['POST'])
def insert_admin():
    data_admin = request.get_json()

    data_admin['password'] = bcrypt.generate_password_hash(str(data_admin['password']))

    new_admin = Admin.insert_admin(data_admin)
    return jsonify({ "admin": new_admin })

@user_bp.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    data_admin = request.get_json()

    # Obtener admin desde la base de datos
    db_admin = Admin.get_admin_by_email(data_admin['email'])

    if not db_admin:
        return jsonify({ "error": 'Admin no registrado' }), 404

    if not len(db_admin):
        return jsonify({ "error": 'Admin no registrado' }), 404

    compare_pass = bcrypt.check_password_hash(db_admin['password'], str(data_admin['password']))

    if not compare_pass:
        return jsonify({ "error": 'Contraseña incorrecta' }), 400

    # Crear el token
    access_token = create_access_token(
        identity=str(db_admin['id']),
        additional_claims={ "role": "admin" },
        expires_delta=timedelta(hours=2), #el token dura 2 horas
    )

    return jsonify({ 
        "access": True,
        "token": access_token,
        "admin": {
            "id": db_admin['id'],
            "email": db_admin['email'],
        }
     }), 200

# Ruta protegida para acceder SOLO con el token de admin
@user_bp.route('/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    current_admin = get_jwt_identity()
    return jsonify({ "access": f'Access true, admin id: {current_admin}' }), 200

@user_bp.route('/all_users', methods=['GET'])
def all_users():
    all_users = User.get_all_users()
    if not all_users:
        return jsonify({ "error": 'No hay users registrados' }), 404
    return jsonify({ "all_users": all_users }), 200