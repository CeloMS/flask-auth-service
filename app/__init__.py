from flask import Flask, jsonify
import logging
from app.database import load_db
from app.exceptions import AppError
from app.routes.route_user import user_bp
from app.routes.route_otp import otp_bp
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

def load_env():
    env_path = find_dotenv()
    if env_path:
        load_dotenv(env_path)
    else:
        logging.warning("No .env file found, attempting to retrieve template")
        template_path = Path("app/models/template.env")
        target_path = Path(".env")
        if not target_path.exists():
            if template_path.exists():
                logging.info("template.env copied successfully."
                    "Don't forget to configure it with your own credentials.")
                target_path.write_text(template_path.read_text())
            else:
                logging.warning("No template file found. Creating an empty .env file."
                    "Please check the needed .env variables in the GitHub repository.")
                target_path.touch()
        load_dotenv(str(target_path))
        
def create_app():
    app = Flask(__name__)
    
    def handle_app_error(e):
        return jsonify({"error": e.message}), e.status_code
    
    app.register_error_handler(AppError, handle_app_error)

    app.register_blueprint(user_bp)
    app.register_blueprint(otp_bp)
    return app


def start():
    load_env()
    load_db()
    app = create_app()
    return app

