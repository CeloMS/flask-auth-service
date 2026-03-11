from flask import Blueprint, jsonify, request
from app.database import SessionLocal
import app.services.otp_service as otps

otp_bp = Blueprint('otp', __name__, url_prefix='/otps')

@otp_bp.route('/<int:user_id>', methods = ['POST'])
def add(user_id):
    try: 
        with SessionLocal() as db:
            token = otps.create(user_id)
            if token is None:
                return jsonify({"error": "User not found"}), 404
            return jsonify({"otp": token}), 201
    except Exception as e:
        return jsonify({"error": f"Something has gone wrong\n{e}"}), 500

@otp_bp.route('/<int:user_id>', methods = ['GET'])
def get(user_id):
    try: 
        with SessionLocal() as db:
            otp = otps.get(user_id)
            if otp is None:
                return jsonify({"error": "User don't have any generated otp"}), 404
            return jsonify(otp.to_dict()), 200
    except Exception as e:
        return jsonify({"error": f"Something has gone wrong\n{e}"}), 500

@otp_bp.route('/<int:user_id>', methods = ['DELETE'])
def delete(user_id):
    try: 
        with SessionLocal() as db:
            result = otps.remove(user_id)
            if result is None:
                return jsonify({"error": "User does not have otp"}), 404
            return '', 204
    except Exception as e:
        return jsonify({"error": f"Something has gone wrong\n{e}"}), 500

@otp_bp.route('<int:user_id>/verify/', methods=['POST'])
def verify(user_id):
    try: 
        with SessionLocal() as db:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            otp = data.get("otp")
            if not otp:
                return jsonify({"error": "Missing 'otp' field"}), 400
            if otps.validate_otp(user_id=user_id, code=otp):
                return jsonify({
                    "message": "OTP verified successfully"
                }), 200
            return jsonify({
                "error": "Invalid or expired OTP"
            }), 401
    except Exception as e:
        return jsonify({"error": f"Something has gone wrong\n{e}"}), 500