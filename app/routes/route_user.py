from flask import Blueprint, jsonify, request
import app.services.user_service as user_service
from app.exceptions import BadRequest
user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/', methods = ['POST'])
def add():
    data = request.get_json()
    if not data:
        raise BadRequest("No data provided")
    try:
        return jsonify(user_service.insert(data['email'], data['password']).to_dict()), 201
    except KeyError as err:
        raise BadRequest(f"Missing argument: {err.args[0]}")

@user_bp.route('/<int:user_id>', methods = ['GET'])
def get(user_id):
    user = user_service.get_id(user_id)
    return jsonify(user.to_dict()), 200
    

@user_bp.route('/<int:user_id>', methods = ['PUT'])
def update(user_id):
    data = request.get_json()
    if not data:
        raise BadRequest("No data provided")
    try:
        user = user_service.update_data(user_id, data)
        return jsonify(user.to_dict()), 200
    except KeyError as err:
        raise BadRequest(f"Missing argument: {err.args[0]}")

@user_bp.route('/<int:user_id>', methods = ['DELETE'])
def delete(user_id):
    user_service.delete_id(user_id)
    return '', 204