from flask import jsonify
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError


def register_error_handlers(app):
    """
    Регистрирует обработчики ошибок для приложения
    :param app: Экземпляр Flask
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': error.description
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required'
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'error': 'Forbidden',
            'message': 'You do not have access to this resource'
        }), 403

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500

    @app.errorhandler(SQLAlchemyError)
    def handle_db_error(error):
        return jsonify({
            'error': 'Database Error',
            'message': 'An error occurred while accessing the database'
        }), 500

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        return jsonify({
            'error': 'Validation Error',
            'message': str(error)
        }), 400