from flask import Blueprint, jsonify, request
from app.database import SessionLocal
from app.models.user import User
from datetime import datetime, UTC

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/', methods = ['POST'])
def create():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        with SessionLocal() as db:
            if db.query(User).filter_by(email=data['email']).first():
                return jsonify({"error": f"Email already registered"}), 409
            now = datetime.now(UTC)
            user = User(
                email=data["email"],
                password_hash=data["password_hash"], #Mudar depois de criar o serviço de password para hash
                created_at=now,
                updated_at=now
            )
            db.add(user)
            db.commit()
            return jsonify(user.to_dict()), 201
    except KeyError as err:
        return jsonify({"error": f"Missing argument: {err.args[0]}"}), 400
    except Exception:
        return jsonify({"error": "Something has gone wrong"}), 500
    
@user_bp.route('/', methods = ['GET'])
def get_all():
    try: 
        with SessionLocal() as db:
            users = db.query(User).all()
            return jsonify([u.to_dict() for u in users]), 200
    except Exception:
        return jsonify({"error": "Something has gone wrong"}), 500

@user_bp.route('/<int:user_id>', methods = ['GET'])
def get_user(user_id):
    try:
        with SessionLocal() as db:
            user = db.get(User, user_id)
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
        with SessionLocal() as db:
            user = db.get(User, user_id)
            if user is None:
                return jsonify({"error": "User not found"}), 404
            for k, v in data.items():  #Mudar depois de criar o serviço de password para hash
                if k not in ["id", "created_at"]:
                    setattr(user, k, v)
            user.updated_at = datetime.now(UTC)
            db.commit()
            return jsonify(user.to_dict()), 200
    except KeyError as err:
        return jsonify({"error": f"Missing argument: {err.args[0]}"}), 400
    except Exception:
        return jsonify({"error": "Something has gone wrong"}), 500

@user_bp.route('/<int:user_id>', methods = ['DELETE'])
def delete(user_id):
    try:
        with SessionLocal() as db:
            user = db.get(User, user_id)
            if user is None:
                return jsonify({"error": "User not found"}), 404
            db.delete(user)
            db.commit()
            return '', 204
    except Exception:
        return jsonify({"error": "Something has gone wrong"}), 500