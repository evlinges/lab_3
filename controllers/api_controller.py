from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.services.note_service import NoteService
from app.services.user_service import UserService
from functools import wraps

# Створення Blueprint для REST API
api_bp = Blueprint('api', __name__)


def admin_required(f):
    """Декоратор для перевірки прав адміністратора"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            return jsonify({'error': 'Доступ заборонено. Потрібні права адміністратора.'}), 403
        return f(*args, **kwargs)
    return decorated_function


# ============================================
# CRUD операції для нотаток (Notes)
# ============================================

@api_bp.route('/notes', methods=['GET'])
@login_required
def get_notes():
    """
    GET /api/notes - Отримати список нотаток
    Адміністратор бачить всі нотатки, USER - тільки свої
    """
    if current_user.is_admin():
        notes = NoteService.get_all_notes()
    else:
        notes = NoteService.get_notes_by_user(current_user.id)
    
    return jsonify({
        'success': True,
        'count': len(notes),
        'notes': [note.to_dict() for note in notes]
    }), 200


@api_bp.route('/notes/<int:note_id>', methods=['GET'])
@login_required
def get_note(note_id):
    """
    GET /api/notes/<id> - Отримати конкретну нотатку за ID
    """
    note = NoteService.get_note_by_id(note_id)
    
    if not note:
        return jsonify({'error': 'Нотатку не знайдено'}), 404
    
    # Перевірка прав доступу
    if not NoteService.can_user_modify_note(note, current_user.id, current_user.is_admin()):
        return jsonify({'error': 'Доступ заборонено'}), 403
    
    return jsonify({
        'success': True,
        'note': note.to_dict()
    }), 200


@api_bp.route('/notes', methods=['POST'])
@login_required
def create_note():
    """
    POST /api/notes - Створити нову нотатку
    Body: { "title": "...", "content": "..." }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Відсутні дані у запиті'}), 400
    
    title = data.get('title')
    content = data.get('content')
    
    result = NoteService.create_note(title, content, current_user.id)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({
        'success': True,
        'message': 'Нотатку успішно створено',
        'note': result['note'].to_dict()
    }), 201


@api_bp.route('/notes/<int:note_id>', methods=['PUT'])
@login_required
def update_note(note_id):
    """
    PUT /api/notes/<id> - Оновити нотатку
    Body: { "title": "...", "content": "..." }
    """
    note = NoteService.get_note_by_id(note_id)
    
    if not note:
        return jsonify({'error': 'Нотатку не знайдено'}), 404
    
    # Перевірка прав доступу
    if not NoteService.can_user_modify_note(note, current_user.id, current_user.is_admin()):
        return jsonify({'error': 'Доступ заборонено'}), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Відсутні дані у запиті'}), 400
    
    title = data.get('title')
    content = data.get('content')
    
    result = NoteService.update_note(note, title, content)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({
        'success': True,
        'message': 'Нотатку успішно оновлено',
        'note': result['note'].to_dict()
    }), 200


@api_bp.route('/notes/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    """
    DELETE /api/notes/<id> - Видалити нотатку
    """
    note = NoteService.get_note_by_id(note_id)
    
    if not note:
        return jsonify({'error': 'Нотатку не знайдено'}), 404
    
    # Перевірка прав доступу
    if not NoteService.can_user_modify_note(note, current_user.id, current_user.is_admin()):
        return jsonify({'error': 'Доступ заборонено'}), 403
    
    NoteService.delete_note(note)
    
    return jsonify({
        'success': True,
        'message': 'Нотатку успішно видалено'
    }), 200


# ============================================
# CRUD операції для користувачів (тільки для ADMIN)
# ============================================

@api_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    """
    GET /api/users - Отримати список користувачів (тільки ADMIN)
    """
    users = UserService.get_all_users()
    
    return jsonify({
        'success': True,
        'count': len(users),
        'users': [user.to_dict() for user in users]
    }), 200


@api_bp.route('/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    """
    GET /api/users/<id> - Отримати конкретного користувача (тільки ADMIN)
    """
    user = UserService.get_user_by_id(user_id)
    
    if not user:
        return jsonify({'error': 'Користувача не знайдено'}), 404
    
    return jsonify({
        'success': True,
        'user': user.to_dict()
    }), 200


@api_bp.route('/users', methods=['POST'])
@admin_required
def create_user():
    """
    POST /api/users - Створити нового користувача (тільки ADMIN)
    Body: { "username": "...", "email": "...", "password": "...", "role": "USER/ADMIN" }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Відсутні дані у запиті'}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'USER')
    
    result = UserService.create_user(username, email, password, role)
    
    if not result['success']:
        return jsonify({'error': result['error']}), 400
    
    return jsonify({
        'success': True,
        'message': 'Користувача успішно створено',
        'user': result['user'].to_dict()
    }), 201


@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """
    DELETE /api/users/<id> - Видалити користувача (тільки ADMIN)
    """
    user = UserService.get_user_by_id(user_id)
    
    if not user:
        return jsonify({'error': 'Користувача не знайдено'}), 404
    
    # Заборонити видалення самого себе
    if user.id == current_user.id:
        return jsonify({'error': 'Не можна видалити самого себе'}), 400
    
    UserService.delete_user(user)
    
    return jsonify({
        'success': True,
        'message': 'Користувача успішно видалено'
    }), 200


# ============================================
# Статистика та інформація
# ============================================

@api_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats():
    """
    GET /api/stats - Отримати статистику (тільки ADMIN)
    """
    stats = NoteService.get_statistics()
    users_count = len(UserService.get_all_users())
    
    return jsonify({
        'success': True,
        'stats': {
            'total_users': users_count,
            'total_notes': stats['total_notes']
        }
    }), 200


@api_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """
    GET /api/me - Отримати інформацію про поточного користувача
    """
    return jsonify({
        'success': True,
        'user': current_user.to_dict()
    }), 200

