from datetime import datetime, timedelta, UTC
from app.models.user import User
import jwt
import os
from bcrypt import checkpw

SECRET = os.getenv("JWT_SECRET")
TOKEN_EXP = os.getenv("JWT_EXPTIME")

def login(db, email: str, password: str):
    user = db.query(User).filter_by(email=email).first()
    if user is None:
        return None
    if not checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return None
    if not user.validated:
        return 
    token = jwt.encode(
        {
            "sub": user.id,
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + timedelta(hours=int(TOKEN_EXP))
        },
        SECRET,
        algorithm="HS256"
    )
    return token