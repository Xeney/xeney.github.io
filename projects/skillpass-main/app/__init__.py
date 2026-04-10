from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, войдите, чтобы увидеть эту страницу.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    # Импортируем модели
    from app import models
    
    # Импортируем и регистрируем blueprints
    from app.routes import auth, main, profile, roadmap, constructor, pages
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(roadmap.bp)
    app.register_blueprint(pages.bp)
    app.register_blueprint(constructor.bp)

    with app.app_context():
        db.create_all()

        # Импортируем и инициализируем админку
        from app import admin
        admin.init_admin(app)

    return app
