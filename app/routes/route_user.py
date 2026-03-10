from flask import Blueprint, jsonify, request
import app.services.user_service as us

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/', methods = ['POST'])
def add():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        return jsonify(us.insert(data['email'], data['password']).to_dict()), 201
    except KeyError as err:
        return jsonify({"error": f"Missing argument: {err.args[0]}"}), 400
    except Exception as er:
        return jsonify({"error": f"Something has gone wrong: {er}"}), 500
    
@user_bp.route('/', methods = ['GET'])
def get_all():
    try: 
        return jsonify(us.get_all()), 200
    except Exception:
        return jsonify({"error": "Something has gone wrong"}), 500

@user_bp.route('/<int:user_id>', methods = ['GET'])
def get(user_id):
    try:
        user = us.get_id(user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user.to_dict()), 200
    except Exception:
        return jsonify({"error": "Something has gone wrong"}), 500

@user_bp.route('/<int:user_id>', methods = ['PUT'])
def update(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        user = us.update_data(user_id, data)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user.to_dict()), 200
    except KeyError as err:
        return jsonify({"error": f"Missing argument: {err.args[0]}"}), 400
    except Exception:
        return jsonify({"error": "Something has gone wrong"}), 500

@user_bp.route('/<int:user_id>', methods = ['DELETE'])
def delete(user_id):
    try:
        response = us.delete_id(user_id)
        if response is None:
            return jsonify({"error": "User not found"}), 404
        return response, 204
    except Exception:
        return jsonify({"error": "Something has gone wrong"}), 500