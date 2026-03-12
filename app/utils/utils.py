import bcrypt

def transform_to_hash(text):
    return bcrypt.hashpw(text.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
