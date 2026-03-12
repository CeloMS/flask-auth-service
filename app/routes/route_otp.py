from flask import Blueprint, jsonify, request
import app.services.otp_service as otp_service

otp_bp = Blueprint('otp', __name__, url_prefix='/otps')

@otp_bp.route('/<int:user_id>', methods = ['POST'])
def add(user_id):
    try: 
        token = otp_service.create(user_id)
        return jsonify({"otp": token}), 201
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@otp_bp.route('/<int:user_id>', methods = ['GET'])
def get(user_id):
    try: 
        otp = otp_service.get(user_id)
        return jsonify(otp.to_dict()), 200
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@otp_bp.route('/<int:user_id>', methods = ['DELETE'])
def delete(user_id):
    try: 
        if otp_service.remove(user_id):
            return '', 204
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@otp_bp.route('<int:user_id>/verify/', methods=['POST'])
def verify(user_id):
    try: 
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        otp = data.get("otp")
        if not otp:
            return jsonify({"error": "Missing 'otp' field"}), 400
        if otp_service.validate_otp(user_id=user_id, code=otp):
                return jsonify({
                    "message": "OTP verified successfully"
                }), 200
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500