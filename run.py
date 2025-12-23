#!/usr/bin/env python3
"""
Точка входу для запуску Flask застосунку
"""

from app import create_app, db
from app.models import User, Note
from app.services.user_service import UserService

app = create_app()


@app.cli.command()
def init_db():
    """Ініціалізувати базу даних з тестовими даними"""
    with app.app_context():
        # Видалити всі таблиці та створити заново
        db.drop_all()
        db.create_all()
        
        # Створити тестових користувачів
        print("Створення тестових користувачів...")
        
        # Адміністратор
        admin_result = UserService.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='ADMIN'
        )
        
        if admin_result['success']:
            print(f"✓ Створено адміністратора: admin / admin123")
        
        # Звичайний користувач
        user_result = UserService.create_user(
            username='user',
            email='user@example.com',
            password='user123',
            role='USER'
        )
        
        if user_result['success']:
            print(f"✓ Створено користувача: user / user123")
        
        # Створити тестові нотатки
        print("\nСтворення тестових нотаток...")
        
        from app.services.note_service import NoteService
        
        if admin_result['success']:
            admin_id = admin_result['user'].id
            NoteService.create_note(
                title='Привітання',
                content='Ласкаво просимо до системи управління нотатками! Це тестова нотатка від адміністратора.',
                user_id=admin_id
            )
            print("✓ Створено нотатку для адміністратора")
        
        if user_result['success']:
            user_id = user_result['user'].id
            NoteService.create_note(
                title='Моя перша нотатка',
                content='Це моя перша нотатка в системі. Тут я можу зберігати важливу інформацію.',
                user_id=user_id
            )
            NoteService.create_note(
                title='Список справ',
                content='1. Зробити лабораторну роботу\n2. Протестувати API\n3. Написати звіт',
                user_id=user_id
            )
            print("✓ Створено нотатки для користувача")
        
        print("\n✅ База даних успішно ініціалізована!")


@app.shell_context_processor
def make_shell_context():
    """Додати змінні до контексту Flask shell"""
    return {
        'db': db,
        'User': User,
        'Note': Note,
        'UserService': UserService
    }


if __name__ == '__main__':
    # Запустити сервер у режимі розробки
    app.run(debug=True, host='0.0.0.0', port=5000)




