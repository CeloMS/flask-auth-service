from flask import Blueprint

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/', methods = ['POST'])
def create():
    pass

@user_bp.route('/', methods = ['GET'])
def get_all():
    pass

@user_bp.route('/<int:user_id>', methods = ['GET'])
def get_user(user_id):
    pass

@user_bp.route('/<int:user_id>>', methods = ['PUT'])
def update(user_id):
    pass

@user_bp.route('/<int:user_id>>', methods = ['DELETE'])
def delete(user_id):
    pass