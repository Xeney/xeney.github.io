from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    # Указываем явный путь к шаблонам
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
    
    app = Flask(__name__, template_folder=template_dir)
    
    # Basic configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBTORS_PER_PAGE'] = 25

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Login configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите в систему.'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.public.routes import bp as public_bp
    app.register_blueprint(public_bp)

    from app.admin.routes import bp as admin_bp
    app.register_blueprint(admin_bp)

    return app