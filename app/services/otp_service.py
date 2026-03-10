import secrets
from datetime import datetime, UTC, timedelta
from app.database import SessionLocal
from app.models.otp import Otp
from app.models.user import User
from app.utils.utils import transform_to_hash

otp_length: int = 6
otp_duration: int = 10
otp_charset = '1234567890'

def generate_token(length: int = otp_length):
    return ''.join(secrets.choice(otp_charset) for _ in range(length))

def create(user_id: int, minutes_valid: int = otp_duration):
    with SessionLocal() as db:
        token = generate_token()
        now = datetime.now(UTC)
        if db.get(User, user_id) is None:
            return None
        entries = db.query(Otp).filter_by(user_id = user_id).all()
        if entries:
            for entry in entries:
                db.delete(entry)
        otp = Otp (
                code = transform_to_hash(token),
                user_id = user_id,
                created_at = now,
                valid_at = now + timedelta(minutes=minutes_valid)
            )
        db.add(otp)
        db.commit()
        return token
    
def remove(user_id):
    with SessionLocal() as db:
        user = db.get(User, user_id)
        if user is None:
            return None   
        entries = db.query(Otp).filter_by(user_id = user_id).all()
        if entries:
            for entry in entries:
                db.delete(entry)
        db.commit()
        return True

def get(user_id):
    with SessionLocal() as db:
        return db.query(Otp).filter_by(user_id=user_id).first()
    
def validate_otp(code: str, user_id: int, delete_after_validation: bool = False, renew_if_fail: bool = True) -> bool:
    pass