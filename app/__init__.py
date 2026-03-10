from flask import Flask
import logging
from app.database import load_db
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

def start():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    app.register_blueprint(otp_bp)
    load_db()
    load_env()
    return app