from flask import Blueprint, jsonify, request
from app.exceptions import AppError
import app.services.otp_service as otp_service

otp_bp = Blueprint('otp', __name__, url_prefix='/otps')

@otp_bp.route('/<int:user_id>', methods = ['POST'])
def add(user_id):
    token = otp_service.create(user_id, None)
    return jsonify({"otp": token}), 201

@otp_bp.route('/<int:user_id>', methods = ['GET'])
def get(user_id):
    otp = otp_service.get(user_id)
    return jsonify(otp.to_dict()), 200
    
@otp_bp.route('/<int:user_id>', methods = ['DELETE'])
def delete(user_id):
    if otp_service.remove(user_id):
            return '', 204

@otp_bp.route('/<int:user_id>/verify/', methods=['POST'])
def verify(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    otp = data.get("otp")
    if not otp:
        return jsonify({"error": "Missing 'otp' field"}), 400
    if otp_service.validate_otp(user_id=user_id, code=otp):
        return jsonify({"message": "OTP verified successfully"}), 200