from werkzeug.security import generate_password_hash, check_password_hash

from yandexform.database import db
from yandexform.models.user import User


def register_user(username, password):
    """
    Регистрация нового пользователя
    :param username: Логин
    :param password: Пароль (открытый текст)
    :return: Созданный пользователь
    """

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        raise ValueError('Пользователь с таким логином уже существует')


    hashed_password = generate_password_hash(password)


    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return new_user


def authenticate_user(username, password):
    """
    Аутентификация пользователя
    :param username: Логин
    :param password: Пароль (открытый текст)
    :return: Пользователь, если данные верны, иначе None
    """
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None