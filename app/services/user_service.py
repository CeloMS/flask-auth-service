from app.repository import user as userbd
from app.exceptions import EmailAlreadyRegistered, UserNotFound
from app.utils.utils import transform_to_hash

blacklist = {"id", "created_at"}

def insert(email, password):
    if userbd.get_by_email(email=email) is not None:
        raise EmailAlreadyRegistered()
    return userbd.create(email=email, password_hash=transform_to_hash(password))

def get_id(user_id):
    user = userbd.get_by_id(user_id)
    if user is None:
        raise UserNotFound()
    return user
     
def update_data(user_id, data):
    data = {k: v for k, v in data.items() if k not in blacklist}
    if "password" in data:
        data["password_hash"] = transform_to_hash(data["password"])
        del data["password"]
    user = userbd.update_by_id(user_id=user_id, data=data)
    if user is None:
        raise UserNotFound()
    return user

def delete_id(user_id):
    user = userbd.remove_by_id(user_id=user_id)
    if user is None:
        raise UserNotFound()
    return user