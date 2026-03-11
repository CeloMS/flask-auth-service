from flask import Blueprint, jsonify, request
from app.database import SessionLocal
import app.services.login_service as logins

login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_bp.route('/login', methods=['POST'])
def login():
    try: 
        with SessionLocal() as db:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")
            result = logins.login(email, password)
            if result is None:
                return jsonify({"error": "Invalid credentials"}), 401
            if result == "EMAIL_NOT_CONFIRMED":
                return jsonify({"error": "Email not confirmed. Please verify your email."}), 403

            return jsonify({
                "token": result
            }), 200
    except Exception as e:
        return jsonify({"error": f"Something has gone wrong\n{e}"}), 500