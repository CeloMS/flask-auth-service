from flask import Blueprint, jsonify, request
import app.services.otp_service as otp_service
from app.exceptions import BadRequest

otp_bp = Blueprint('otp', __name__, url_prefix='/otps')

@otp_bp.route('/<int:user_uuid>', methods = ['POST'])
def add(user_uuid):
    token = otp_service.create_by_uuid(user_uuid, None)
    return jsonify({"otp": token}), 201
    
@otp_bp.route('/<int:user_uuid>', methods = ['DELETE'])
def delete(user_uuid):
    if otp_service.remove_by_uuid(user_uuid):
            return '', 204

@otp_bp.route('/<int:user_uuid>/verify', methods=['POST'])
def verify(user_uuid):
    data = request.get_json()
    if not data:
        raise BadRequest("No data provided")
    otp = data.get("otp")
    if not otp:
        raise BadRequest("Missing 'otp' field")
    if otp_service.validate_otp_by_uuid(user_uuid=user_uuid, user_otp=otp):
        return jsonify({"message": "OTP verified successfully"}), 200