import bcrypt, os

def transform_to_hash(text):
    return bcrypt.hashpw(text.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def get_config(value, default_value):
    data = os.getenv(value)
    if data is None:
        return default_value
    return data