from flask import Flask
from app.database import load_db
from app.routes.route_user import user_bp

def start():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    load_db()
    return app