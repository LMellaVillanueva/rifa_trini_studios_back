from flask import jsonify, Blueprint, request
from app.models.Voucher import Voucher
from app import app

voucher_bp = Blueprint('voucher_bp', __name__)


@voucher_bp.route('/validate', methods=['POST'])
def validate_voucher():
    data_voucher = request.get_json()
    voucher_existant = Voucher.get_voucher_by_id(data_voucher['id'])
    if not voucher_existant:
        return jsonify({ "error": 'Este voucher no existe' }), 404
    
    verif_voucher = Voucher.verif_voucher(data_voucher)
    
    return jsonify({ "numbers": verif_voucher }), 200

@voucher_bp.route('/elim', methods=['POST'])
def elim_vouchers():
    vouchers_deleted = Voucher.delete_vouchers()
    return jsonify({ "message": vouchers_deleted }), 200