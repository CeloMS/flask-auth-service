from datetime import datetime, timedelta, UTC
from app.models.user import User
import jwt
from bcrypt import checkpw
from app.utils.utils import get_config

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
            "exp": datetime.now(UTC) + timedelta(hours=int(get_config("JWT_EXPTIME", 10)))
        },
        get_config("JWT_SECRET", "DEFAULT_VALUE"),
        algorithm="HS256"
    )
    return token