import secrets, os
from datetime import datetime, UTC, timedelta
import app.repository.otp as otp_repository
import app.repository.user as user_repository
from app.exceptions import UserNotFound, InvalidOtp, OtpExpired, OtpNotFound
from bcrypt import checkpw

OTP_LENGTH: int = os.getenv("OTP_LENGTH")
OTP_DURATION: int = os.getenv("OTP_DURATION")
OTP_CHARSET = os.getenv("OTP_CHARSET")

def generate_token(length: int = OTP_LENGTH):
    return ''.join(secrets.choice(OTP_CHARSET) for _ in range(length))

def create(user_id: int, minutes_valid: int = int(OTP_DURATION)):
    token = generate_token()
    if user_repository.get_by_id(user_id=user_id) is None:
        raise UserNotFound()
    otp_repository.clean_user_id(user_id=user_id)
    return otp_repository.create(user_id, token,  datetime.now(UTC)+ timedelta(minutes=minutes_valid))
    
def remove(user_id):
    otp = otp_repository.remove_by_user_id(user_id)
    if otp is None:
        raise InvalidOtp()
    return True

def get(user_id):
    otp = otp_repository.get_by_user_id(user_id=user_id)
    if otp is None:
        raise OtpNotFound()
    
def validate_otp(user_id: int, otp: str) -> bool:
    otp = user_repository.get_by_id(user_id=user_id)
    if otp is None:
        raise InvalidOtp()
    now = datetime.now(UTC)
    if now > otp.valid_at:
        user_repository.remove_by_id(user_id=user_id)
        raise OtpExpired()
    if not checkpw(otp.encode('utf-8'), otp.code.decode('utf-8')):
        raise InvalidOtp()
    user_repository.update_by_id(user_id=user_id, data={'validated': True})
    return True