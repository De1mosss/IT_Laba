from flask import Blueprint, request, jsonify
from yandexform.services.response_service import submit_response, get_responses_for_form
from yandexform.utils.auth_utils import login_required

response_bp = Blueprint('response', __name__)


@response_bp.route('/responses/<int:form_id>', methods=['POST'])
@login_required
def submit_response_route(current_user, form_id):
    """Отправка ответа на форму"""
    data = request.get_json()
    answers = data.get('answers')

    if not answers:
        return jsonify({'error': 'Answers are required'}), 400

    try:
        response = submit_response(form_id, current_user.id, answers)
        return jsonify({
            'id': response.id,
            'form_id': response.form_id,
            'submitted_at': response.submitted_at.isoformat()
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@response_bp.route('/responses/<int:form_id>', methods=['GET'])
@login_required
def get_responses_route(current_user, form_id):
    """Получение всех ответов на форму (только для владельца)"""
    responses = get_responses_for_form(form_id, current_user.id)
    if not responses:
        return jsonify({'error': 'Form not found or access denied'}), 404

    return jsonify([{
        'id': r.id,
        'user_id': r.user_id,
        'answers': r.answers,
        'submitted_at': r.submitted_at.isoformat()
    } for r in responses]), 200