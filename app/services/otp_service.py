import secrets
from datetime import datetime, UTC, timedelta
import app.repository.otp as otp_repository
import app.repository.user as user_repository
from app.exceptions import UserNotFound, InvalidOtp, OtpExpired, OtpNotFound
from bcrypt import checkpw
from app.utils.utils import get_config, transform_to_hash

def generate_token(length):
    if length is None:
        length = get_config("OTP_LENGTH", 6)
    return ''.join(secrets.choice(get_config("OTP_CHARSET"), "123456789") for _ in range(int(length)))

def create(user_id: int, minutes_valid):
    if minutes_valid is None:
        minutes_valid = get_config("OTP_DURATION", 15)
    token = generate_token()
    if user_repository.get_by_id(user_id=user_id) is None:
        raise UserNotFound()
    otp_repository.clean_user_id(user_id=user_id)
    return otp_repository.create(user_id, transform_to_hash(token),  datetime.now(UTC)+ timedelta(minutes=int(minutes_valid)))
    
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
    otp = otp_repository.get_by_user_id(user_id=user_id)
    if otp is None:
        raise InvalidOtp()
    now = datetime.now(UTC)
    if now > otp.valid_at:
        otp_repository.remove_by_user_id(user_id=user_id)
        raise OtpExpired()
    if not checkpw(otp.encode('utf-8'), otp.code.decode('utf-8')):
        raise InvalidOtp()
    user_repository.update_by_id(user_id=user_id, data={'validated': True})
    return True