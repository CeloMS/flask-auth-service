import secrets, logging
from datetime import datetime, UTC, timedelta
from app.database import SessionLocal
from app.models.otp import Otp
from app.models.user import User

def generate_otp(id, length: int = 6, minutes_valid: int = 10):
    try:
        with SessionLocal() as db:
            token = ''.join(secrets.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(length))
            user = db.get(User, id)
            if user is None:
                logging.exception("User id not found")
                return None
            entries = db.query(Otp).filter_by(user_id = user.id)
            if entries:
                for entry in entries:
                    db.delete(entry)
                    db.commit()
            now = datetime.now(UTC)
            otp = Otp (
                code = token,
                user_id = user.id,
                created_at = now,
                valid_at = now + timedelta(minutes=minutes_valid)
            )
            db.add(otp)
            db.commit()
            return token
    except Exception as e:
        logging.exception(f"Error trying to load your database: \n{e}")