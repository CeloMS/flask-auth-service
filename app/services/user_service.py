from app.models.user import User
from app.utils.utils import transform_to_hash
from app.database import SessionLocal
from datetime import datetime, UTC

def insert(email, password):
    now = datetime.now(UTC)
    with SessionLocal() as db:
        user = User(email=email,password_hash=transform_to_hash(password),created_at=now,updated_at=now)
        db.add(user)
        db.commit()
        return user
    
def get_id(user_id):
    with SessionLocal() as db:
        return db.get(User, user_id)
     
def update_data(user_id, data):
    with SessionLocal() as db:
        user = db.get(User, user_id)
        if user is None:
            return None   
        for k, v in data.items():
            if k not in ["id", "created_at"]:
                setattr(user, k, v)
            if k in ["password_hash"]:
                setattr(user, k, transform_to_hash(data['password']))
            user.updated_at = datetime.now(UTC)
            db.commit()

def delete_id(user_id):
    with SessionLocal() as db:
        user = db.get(User, user_id)
        if user is None:
            return None
        db.delete(user)
        db.commit()
        return ''