from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    """Модель користувача з підтримкою автентифікації"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='USER')  # USER або ADMIN
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Зв'язок один-до-багатьох з нотатками
    notes = db.relationship('Note', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Серіалізація об'єкта в словник (для JSON)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def is_admin(self):
        """Перевірка чи є користувач адміністратором"""
        return self.role == 'ADMIN'

