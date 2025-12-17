from app import bcrypt
from app.models.user import User
from app.repositories.user_repository import UserRepository
from typing import Optional, List, Dict


class UserService:
    """Service для бізнес-логіки роботи з користувачами"""
    
    @staticmethod
    def create_user(username: str, email: str, password: str, role: str = 'USER') -> Dict:
        """Створити нового користувача з валідацією"""
        
        # Валідація
        if not username or len(username) < 3:
            return {'success': False, 'error': 'Username має містити мінімум 3 символи'}
        
        if not email or '@' not in email:
            return {'success': False, 'error': 'Невалідний email'}
        
        if not password or len(password) < 6:
            return {'success': False, 'error': 'Пароль має містити мінімум 6 символів'}
        
        if role not in ['USER', 'ADMIN']:
            return {'success': False, 'error': 'Невалідна роль'}
        
        # Перевірка чи існує користувач
        if UserRepository.exists_by_username(username):
            return {'success': False, 'error': 'Користувач з таким username вже існує'}
        
        if UserRepository.exists_by_email(email):
            return {'success': False, 'error': 'Користувач з таким email вже існує'}
        
        # Хешування пароля
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Створення користувача
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role
        )
        
        created_user = UserRepository.create(user)
        return {'success': True, 'user': created_user}
    
    @staticmethod
    def authenticate(username: str, password: str) -> Optional[User]:
        """Автентифікація користувача"""
        user = UserRepository.find_by_username(username)
        
        if user and bcrypt.check_password_hash(user.password_hash, password):
            return user
        
        return None
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """Отримати користувача за ID"""
        return UserRepository.find_by_id(user_id)
    
    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        """Отримати користувача за username"""
        return UserRepository.find_by_username(username)
    
    @staticmethod
    def get_all_users() -> List[User]:
        """Отримати всіх користувачів"""
        return UserRepository.find_all()
    
    @staticmethod
    def update_user(user: User, **kwargs) -> Dict:
        """Оновити користувача"""
        
        if 'email' in kwargs:
            email = kwargs['email']
            if not email or '@' not in email:
                return {'success': False, 'error': 'Невалідний email'}
            
            # Перевірка чи email не зайнятий іншим користувачем
            existing = UserRepository.find_by_email(email)
            if existing and existing.id != user.id:
                return {'success': False, 'error': 'Email вже зайнятий'}
            
            user.email = email
        
        if 'role' in kwargs:
            role = kwargs['role']
            if role not in ['USER', 'ADMIN']:
                return {'success': False, 'error': 'Невалідна роль'}
            user.role = role
        
        if 'password' in kwargs:
            password = kwargs['password']
            if len(password) < 6:
                return {'success': False, 'error': 'Пароль має містити мінімум 6 символів'}
            user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        updated_user = UserRepository.update(user)
        return {'success': True, 'user': updated_user}
    
    @staticmethod
    def delete_user(user: User) -> None:
        """Видалити користувача"""
        UserRepository.delete(user)

