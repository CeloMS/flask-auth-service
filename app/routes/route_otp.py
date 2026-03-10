from flask import Blueprint, jsonify
import app.services.otp_service as otps

otp_bp = Blueprint('otp', __name__, url_prefix='/otps')


@otp_bp.route('/<int:user_id>', methods = ['POST'])
def add(user_id):
    try:
        token = otps.create(user_id)
        if token is None:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"otp": token}), 201
    except Exception as er:
        return jsonify({"error": f"Something has gone wrong: {er}"}), 500

@otp_bp.route('/<int:user_id>', methods = ['GET'])
def get(user_id):
    try:
        otp = otps.get(user_id)
        if otp is None:
            return jsonify({"error": "User don't have any generated otp"}), 404
        return jsonify(otp.to_dict()), 200
    except Exception:
        return jsonify({"error": "Something has gone wrong"}), 500

@otp_bp.route('/<int:user_id>', methods = ['DELETE'])
def delete(user_id):
    try:
        result = otps.remove(user_id)
        if result is None:
            return jsonify({"error": "User does not have otp"}), 404
        return '', 204
    except Exception:
        return jsonify({"error": "Something has gone wrong"}), 500
