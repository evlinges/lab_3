import os
from datetime import timedelta


class Config:
    """Конфігурація застосунку"""
    
    # Базова директорія проєкту
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Секретний ключ для сесій та CSRF захисту
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Конфігурація бази даних SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    
    # Вимкнення відстеження модифікацій (для економії ресурсів)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Налаштування сесій
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'




