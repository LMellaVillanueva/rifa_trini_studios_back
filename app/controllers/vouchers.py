from flask import jsonify, Blueprint
from app.models.Voucher import Voucher
from app import app

voucher_bp = Blueprint('voucher_bp', __name__)


@voucher_bp.route('/validate/<id>', methods=['GET'])
def validate_voucher(id):
    voucher_existant = Voucher.get_voucher_by_id(id)
    if not voucher_existant:
        return jsonify({ "error": 'Este voucher no existe' }), 404
    
    verif_voucher = Voucher.verif_voucher(id)
    
    return jsonify({ "numbers": verif_voucher }), 200