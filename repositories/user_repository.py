from app import db
from app.models.user import User
from typing import Optional, List


class UserRepository:
    """Repository для роботи з користувачами в базі даних"""
    
    @staticmethod
    def create(user: User) -> User:
        """Створити нового користувача"""
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def find_by_id(user_id: int) -> Optional[User]:
        """Знайти користувача за ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def find_by_username(username: str) -> Optional[User]:
        """Знайти користувача за username"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def find_by_email(email: str) -> Optional[User]:
        """Знайти користувача за email"""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def find_all() -> List[User]:
        """Отримати всіх користувачів"""
        return User.query.all()
    
    @staticmethod
    def update(user: User) -> User:
        """Оновити користувача"""
        db.session.commit()
        return user
    
    @staticmethod
    def delete(user: User) -> None:
        """Видалити користувача"""
        db.session.delete(user)
        db.session.commit()
    
    @staticmethod
    def exists_by_username(username: str) -> bool:
        """Перевірити чи існує користувач з таким username"""
        return User.query.filter_by(username=username).first() is not None
    
    @staticmethod
    def exists_by_email(email: str) -> bool:
        """Перевірити чи існує користувач з таким email"""
        return User.query.filter_by(email=email).first() is not None

