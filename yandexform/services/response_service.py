from yandexform.models.response import Response
from yandexform.models.form import Form
from yandexform.database import db
from yandexform.utils.validation import validate_response


def submit_response(form_id, user_id, answers):
    """
    Отправляет ответ на форму
    :param form_id: ID формы
    :param user_id: ID пользователя, отправившего ответ
    :param answers: Данные ответа (JSON)
    :return: Созданный ответ
    """
    form = Form.query.get(form_id)
    if not form:
        raise ValueError('Форма не найдена')

    validate_response(form.fields, answers)

    new_response = Response(
        form_id=form_id,
        user_id=user_id,
        answers=answers
    )
    db.session.add(new_response)
    db.session.commit()
    return new_response


def get_responses_for_form(form_id, user_id):
    """
    Возвращает все ответы на форму (только для владельца формы)
    :param form_id: ID формы
    :param user_id: ID пользователя (владельца)
    :return: Список ответов
    """
    form = Form.query.get(form_id)
    if not form or form.owner_id != user_id:
        return None
    return Response.query.filter_by(form_id=form_id).all()