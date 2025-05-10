from flask import Blueprint, request, jsonify
from yandexform.services.form_service import create_form, get_form_by_id, update_form, delete_form, get_user_forms
from yandexform.utils.auth_utils import login_required

form_bp = Blueprint('form', __name__)


@form_bp.route('/forms', methods=['POST'])
@login_required
def create_form_route(current_user):
    data = request.get_json()
    title = data.get('title')
    fields = data.get('fields')

    if not title or not fields:
        return jsonify({'error': 'Title and fields are required'}), 400

    form = create_form(current_user.id, title, fields)
    return jsonify({
        'id': form.id,
        'title': form.title,
        'fields': form.fields
    }), 201


@form_bp.route('/forms/<int:form_id>', methods=['GET'])
@login_required
def get_form_route(current_user, form_id):
    form = get_form_by_id(form_id)
    if not form or form.owner_id != current_user.id:
        return jsonify({'error': 'Form not found'}), 404
    return jsonify({
        'id': form.id,
        'title': form.title,
        'fields': form.fields
    }), 200


@form_bp.route('/forms/<int:form_id>', methods=['PUT'])
@login_required
def update_form_route(current_user, form_id):
    data = request.get_json()
    updated_form = update_form(form_id, current_user.id, **data)
    if not updated_form:
        return jsonify({'error': 'Form not found or access denied'}), 404
    return jsonify({
        'id': updated_form.id,
        'title': updated_form.title,
        'fields': updated_form.fields
    }), 200


@form_bp.route('/forms/<int:form_id>', methods=['DELETE'])
@login_required
def delete_form_route(current_user, form_id):
    if delete_form(form_id, current_user.id):
        return jsonify({'message': 'Form deleted'}), 200
    return jsonify({'error': 'Form not found or access denied'}), 404


@form_bp.route('/forms', methods=['GET'])
@login_required
def get_user_forms_route(current_user):
    forms = get_user_forms(current_user.id)
    return jsonify([{
        'id': form.id,
        'title': form.title,
        'fields': form.fields
    } for form in forms]), 200