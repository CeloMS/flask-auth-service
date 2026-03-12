from datetime import datetime, timedelta, UTC
import jwt
from bcrypt import checkpw
import app.repository.user as user_repository
from app.exceptions import UserNotFound, InvalidCredentials, EmailNotConfirmed
from app.config import Settings

def login(email: str, password: str):
    user = user_repository.get_by_email(email)
    if user is None:
        raise UserNotFound()
    if not checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise InvalidCredentials()
    if not user.validated:
        raise EmailNotConfirmed()
    token = jwt.encode(
        {
            "sub": str(user.id),
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + timedelta(hours=Settings.JWT_EXPTIME)
        },
        Settings.JWT_SECRET,
        algorithm="HS256"
    )
    return token