import secrets
from datetime import datetime, UTC, timedelta
import app.repository.otp as otp_repository
import app.repository.user as user_repository
from app.exceptions import UserNotFound, InvalidOtp, OtpExpired, OtpNotFound
from bcrypt import checkpw
from app.utils.utils import transform_to_hash
from app.config import settings

def generate_token(length=None):
    if length is None:
        length = settings.OTP_LENGTH
    charset = settings.OTP_CHARSET
    return ''.join(secrets.choice(charset) for _ in range(int(length)))

def create(user_id: int, minutes_valid=None):
    if minutes_valid is None:
        minutes_valid = settings.OTP_DURATION
    token = generate_token()
    if user_repository.get_by_id(user_id=user_id) is None:
        raise UserNotFound()
    otp_repository.clean_user_id(user_id=user_id)
    otp_repository.create(user_id, transform_to_hash(token),  datetime.now(UTC)+ timedelta(minutes=int(minutes_valid)))
    return token

def create_by_uuid(user_uuid: int, minutes_valid=None):
    if minutes_valid is None:
        minutes_valid = settings.OTP_DURATION
    user = user_repository.get_by_uuid(user_uuid=user_uuid)
    if user is None:
        raise UserNotFound()
    return create(user_id=user.id, minutes_valid=minutes_valid)

def remove(user_id):
    otp = otp_repository.remove_by_user_id(user_id)
    if otp is None:
        raise InvalidOtp()
    return True

def remove_by_uuid(user_uuid):
    user = user_repository.get_by_uuid(user_uuid=user_uuid)
    if user is None:
        raise UserNotFound()
    return remove(user_id=user.id)
    user = user_repository.get_by_uuid(user_uuid=user_uuid)
    if user is None:
        raise UserNotFound()
    return get(user_id=user.id)

def validate_otp(user_id: int, user_otp: str) -> bool:
    otp = otp_repository.get_by_user_id(user_id=user_id)
    if otp is None:
        raise InvalidOtp()
    now = datetime.now(UTC)
    if now > otp.valid_at:
        otp_repository.remove_by_user_id(user_id=user_id)
        raise OtpExpired()
    if not checkpw(user_otp.encode('utf-8'), otp.code.encode('utf-8')):
        raise InvalidOtp()
    user_repository.update_by_id(user_id=user_id, data={'validated': True})
    otp_repository.remove_by_user_id(user_id=user_id)
    return True

def validate_otp_by_uuid(user_uuid: int, user_otp: str) -> bool:
    user = user_repository.get_by_uuid(user_uuid=user_uuid)
    if user is None:
        raise UserNotFound()
    return validate_otp(user_id=user.id, user_otp=user_otp)