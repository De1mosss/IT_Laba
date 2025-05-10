from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt_identity, jwt_required
from yandexform.models.user import User


def generate_token(user_id):
    return create_access_token(identity=str(user_id))

def verify_token():
    try:
        verify_jwt_in_request()
        return get_jwt_identity()
    except:
        return None


def login_required(f):
    @wraps(f)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        return f(current_user, *args, **kwargs)
    return wrapper
