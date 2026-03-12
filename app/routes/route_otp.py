from flask import Blueprint, jsonify, request
import app.services.otp_service as otp_service
from app.exceptions import BadRequest

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
        raise BadRequest("No data provided")
    otp = data.get("otp")
    if not otp:
        raise BadRequest("Missing 'otp' field")
    if otp_service.validate_otp(user_id=user_id, user_otp=otp):
        return jsonify({"message": "OTP verified successfully"}), 200