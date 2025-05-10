from flask import Flask
from flask_migrate import Migrate, upgrade
from flask_jwt_extended import JWTManager
from .config import Config
from .database.db import db
from .routes.auth_routes import auth_bp
from .routes.form_routes import form_bp
from .routes.response_routes import response_bp
from .errors import register_error_handlers
import os


migrate = Migrate()

def create_app():
    instance_path = os.path.join(os.path.dirname(__file__), 'instance')
    os.makedirs(instance_path, exist_ok=True)

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.config['JWT_SECRET_KEY'] = Config.SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
    jwt = JWTManager(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # Регистрация Blueprint'ов
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(form_bp, url_prefix='/form')
    app.register_blueprint(response_bp, url_prefix='/api')

    # Swagger
    from flask_swagger_ui import get_swaggerui_blueprint
    swagger_ui = get_swaggerui_blueprint('/api/docs', '/static/swagger.json', config={'app_name': "My API"})
    app.register_blueprint(swagger_ui, url_prefix='/api/docs')

    # HTML Pages
    from flask import render_template

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register')
    def register_page():
        return render_template('register.html')

    @app.route('/login')
    def login_page():
        return render_template('login.html')

    @app.route('/create-form')
    def create_form_page():
        return render_template('create_form.html')

    @app.route('/view-forms')
    def view_forms_page():
        return render_template('view_forms.html')

    @app.route('/fill-form')
    def fill_form_page():
        return render_template('fill_form.html')

    @app.route('/api/users')
    def get_users():
        from flask import jsonify
        return jsonify([{"id": 1, "name": "John Doe"}])

    register_error_handlers(app)

    with app.app_context():
        upgrade()
        db.create_all()

    return app
