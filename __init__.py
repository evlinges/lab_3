from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

# Ініціалізація розширень Flask
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app(config_class=Config):
    """Factory функція для створення та конфігурації застосунку Flask"""
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ініціалізація розширень з застосунком
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    # Налаштування Flask-Login
    login_manager.login_view = 'web.login'
    login_manager.login_message = 'Будь ласка, увійдіть для доступу до цієї сторінки.'
    login_manager.login_message_category = 'info'
    
    # Імпорт моделей (необхідно для створення таблиць)
    from app.models import User, Note
    
    # Реєстрація контролерів (blueprints)
    from app.controllers.api_controller import api_bp
    from app.controllers.web_controller import web_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(web_bp)
    
    # Створення таблиць БД при першому запуску
    with app.app_context():
        db.create_all()
    
    # Callback для завантаження користувача
    @login_manager.user_loader
    def load_user(user_id):
        from app.repositories.user_repository import UserRepository
        return UserRepository.find_by_id(int(user_id))
    
    return app

