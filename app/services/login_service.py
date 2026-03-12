from datetime import datetime, timedelta, UTC
from app.models.user import User
import jwt
from bcrypt import checkpw
import app.repository.user as user_repository
import app.repository.otp as otp_repository
from app.exceptions import UserNotFound, InvalidCredentials, EmailNotConfirmed
from app.utils.utils import get_config

def login(email: str, password: str):
    user = user_repository.get_user_by_email(email)
    if user is None:
        return UserNotFound()
    if not checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return InvalidCredentials()
    if not user.validated:
        return EmailNotConfirmed()
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