from app.database import SessionLocal
from app.models.user import User

def create(email, password_hash):
    with SessionLocal() as db:
        user = User(email=email,password_hash=password_hash)
        try:
            db.add(user)
            db.commit()
            return user
        except Exception:
            db.rollback()
            raise

def remove_by_id(user_id):
    with SessionLocal() as db:
        user = db.get(User, user_id)
        if user is None:
            return None
        try:
            db.delete(user)
            db.commit()
            return True
        except Exception:
            db.rollback()
            raise

def remove_by_email(email):
    with SessionLocal() as db:
        user = db.query(User).filter_by(email=email).first()
        if user is None:
            return None
        try:
            db.delete(user)
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False
    
def update_by_id(user_id, data):
    with SessionLocal() as db:
        user = db.get(User, user_id)
        if user is None:
            return None
        for k, v in data.items():
            setattr(user, k, v)
        try:
            db.commit()
            return user
        except Exception:
            db.rollback()
            raise

def get_by_id(user_id):
    with SessionLocal() as db:
        return db.get(User, user_id)

def get_by_email(email):
    with SessionLocal() as db:
        return db.query(User).filter_by(email=email).first()
