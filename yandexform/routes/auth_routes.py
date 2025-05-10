from flask import Blueprint, request, jsonify
from yandexform.services.auth_service import register_user, authenticate_user
from yandexform.utils.auth_utils import generate_token

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Регистрация нового пользователя"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')


    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400


    new_user = register_user(username, password)
    return jsonify({'message': 'User registered successfully', 'user_id': new_user.id}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Вход в систему"""

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')


    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400


    user = authenticate_user(username, password)
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401


    token = generate_token(user.id)
    return jsonify({'token': token, 'user_id': user.id}), 200