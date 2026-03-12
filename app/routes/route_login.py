from flask import Blueprint, jsonify, request
from app.exceptions import BadRequest
import app.services.login_service as logins

login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_bp.route('/', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        raise BadRequest("No data provided")
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        raise BadRequest("Missing fields")
    result = logins.login(email, password)
    return jsonify({
                "token": result
            }), 200