from flask import Blueprint, jsonify, request
import app.services.user_service as user_service
from app.exceptions import AppError
user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/', methods = ['POST'])
def add():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        return jsonify(user_service.insert(data['email'], data['password']).to_dict()), 201
    except KeyError as err:
        return jsonify({"error": f"Missing argument: {err.args[0]}"}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@user_bp.route('/<int:user_id>', methods = ['GET'])
def get(user_id):
    try:
        user = user_service.get_id(user_id)
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
    

@user_bp.route('/<int:user_id>', methods = ['PUT'])
def update(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        user = user_service.update_data(user_id, data)
        return jsonify(user.to_dict()), 200
    except KeyError as err:
        return jsonify({"error": f"Missing argument: {err.args[0]}"}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@user_bp.route('/<int:user_id>', methods = ['DELETE'])
def delete(user_id):
    try:
        user_service.delete_id(user_id)
        return '', 204
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500