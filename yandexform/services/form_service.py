from yandexform.models.form import Form
from yandexform.database import db
from yandexform.utils.validation import validate_form_fields


def create_form(user_id, title, fields):
    validate_form_fields(fields)

    new_form = Form(title=title, fields=fields, owner_id=user_id)
    db.session.add(new_form)
    db.session.commit()
    return new_form


def get_form_by_id(form_id):
    return Form.query.get(form_id)


def update_form(form_id, user_id, **kwargs):
    form = Form.query.get(form_id)
    if not form or form.owner_id != user_id:
        return None

    if 'title' in kwargs:
        form.title = kwargs['title']
    if 'fields' in kwargs:
        validate_form_fields(kwargs['fields'])
        form.fields = kwargs['fields']

    db.session.commit()
    return form


def delete_form(form_id, user_id):
    form = Form.query.get(form_id)
    if form and form.owner_id == user_id:
        db.session.delete(form)
        db.session.commit()
        return True
    return False


def get_user_forms(user_id):
    return Form.query.filter_by(owner_id=user_id).all()