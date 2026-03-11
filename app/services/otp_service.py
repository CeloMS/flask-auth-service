import secrets, os
from datetime import datetime, UTC, timedelta
from app.database import SessionLocal
from app.models.otp import Otp
from app.models.user import User
from app.utils.utils import transform_to_hash
from bcrypt import checkpw

OTP_LENGTH: int = os.getenv("OTP_LENGTH")
OTP_DURATION: int = os.getenv("OTP_DURATION")
OTP_CHARSET = os.getenv("OTP_CHARSET")

def generate_token(db, length: int = OTP_LENGTH):
    return ''.join(secrets.choice(OTP_CHARSET) for _ in range(length))

def create(db, user_id: int, minutes_valid: int = int(OTP_DURATION)):
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
    
def remove(db, user_id):
    user = db.get(User, user_id)
    if user is None:
        return None   
    entries = db.query(Otp).filter_by(user_id = user_id).all()
    if entries:
        for entry in entries:
            db.delete(entry)
    db.commit()
    return True

def get(db, user_id):
    return db.query(Otp).filter_by(user_id=user_id).first()
    
def validate_otp(db, user_id: int, otp: str) -> bool:
    otp = db.query(Otp).filter_by(user_id=user_id).first()
    if otp is None:
        return False    
    now = datetime.now(UTC)
    if now > otp.valid_at:
        db.delete(otp)
        db.commit()
        return False
    if not checkpw(otp.encode('utf-8'), otp.code.decode('utf-8')):
        return False
    db.get(User, user_id).validated = True
    db.delete(otp)
    db.commit()
    return True