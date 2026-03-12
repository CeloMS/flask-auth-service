from app.database import SessionLocal
from app.models.otp import Otp
from app.models.user import User
from datetime import datetime

def create(user_id:int, token_hash:str, valid_at:datetime):
    with SessionLocal() as db:
        otp = Otp (
            user_id=user_id,
            code=token_hash,
            valid_at=valid_at
        )
        try:
            db.add(otp)
            db.commit()
            return otp
        except Exception:
            db.rollback()
            raise

def get(otp_id):
    with SessionLocal() as db:
        return db.get(Otp, otp_id)
        
def get_by_user_id(user_id):
    with SessionLocal() as db:
        return db.query(Otp).filter_by(user_id=user_id).first()
    
def remove(otp_id):
    with SessionLocal() as db:
        otp = db.get(Otp, otp_id)
        if otp is None:
            return None
        try:
            db.delete(otp)
            db.commit()
            return True
        except Exception:
            db.rollback()
            raise
    
def remove_by_user_id(user_id):
    with SessionLocal() as db:
        otp = db.query(Otp).filter_by(user_id = user_id).first()
        if otp is None:
            return None
        try:
            db.delete(otp)
            db.commit()
            return True
        except Exception:
            db.rollback()
            raise

def clean_user_id(user_id):
    with SessionLocal() as db:
        otps = db.query(Otp).filter_by(user_id = user_id).all()
        if otps:
            for otp in otps:
                db.delete(otp)
        try:
            db.commit()
            return True
        except Exception:
            db.rollback()
            raise