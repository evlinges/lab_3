from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.services.user_service import UserService
from app.services.note_service import NoteService

# Створення Blueprint для веб-інтерфейсу
web_bp = Blueprint('web', __name__)


@web_bp.route('/')
def index():
    """Головна сторінка"""
    if current_user.is_authenticated:
        return redirect(url_for('web.notes'))
    return redirect(url_for('web.login'))


@web_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Сторінка входу"""
    if current_user.is_authenticated:
        return redirect(url_for('web.notes'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Будь ласка, заповніть усі поля', 'error')
            return render_template('login.html')
        
        # Автентифікація
        user = UserService.authenticate(username, password)
        
        if user:
            login_user(user, remember=True)
            flash(f'Ласкаво просимо, {user.username}!', 'success')
            
            # Перенаправлення на початкову сторінку або на notes
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('web.notes'))
        else:
            flash('Невірний логін або пароль', 'error')
    
    return render_template('login.html')


@web_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Сторінка реєстрації"""
    if current_user.is_authenticated:
        return redirect(url_for('web.notes'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        if not all([username, email, password, password_confirm]):
            flash('Будь ласка, заповніть усі поля', 'error')
            return render_template('register.html')
        
        if password != password_confirm:
            flash('Паролі не співпадають', 'error')
            return render_template('register.html')
        
        # Створення користувача
        result = UserService.create_user(username, email, password, role='USER')
        
        if result['success']:
            flash('Реєстрація успішна! Тепер ви можете увійти.', 'success')
            return redirect(url_for('web.login'))
        else:
            flash(result['error'], 'error')
    
    return render_template('register.html')


@web_bp.route('/logout')
@login_required
def logout():
    """Вихід з системи"""
    logout_user()
    flash('Ви успішно вийшли з системи', 'info')
    return redirect(url_for('web.login'))


@web_bp.route('/notes')
@login_required
def notes():
    """Сторінка зі списком нотаток"""
    if current_user.is_admin():
        all_notes = NoteService.get_all_notes()
    else:
        all_notes = NoteService.get_notes_by_user(current_user.id)
    
    return render_template('notes.html', notes=all_notes)


@web_bp.route('/notes/create', methods=['GET', 'POST'])
@login_required
def create_note():
    """Створення нової нотатки"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        result = NoteService.create_note(title, content, current_user.id)
        
        if result['success']:
            flash('Нотатку успішно створено!', 'success')
            return redirect(url_for('web.notes'))
        else:
            flash(result['error'], 'error')
    
    return render_template('note_form.html', mode='create')


@web_bp.route('/notes/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    """Редагування нотатки"""
    note = NoteService.get_note_by_id(note_id)
    
    if not note:
        flash('Нотатку не знайдено', 'error')
        return redirect(url_for('web.notes'))
    
    # Перевірка прав доступу
    if not NoteService.can_user_modify_note(note, current_user.id, current_user.is_admin()):
        flash('Доступ заборонено', 'error')
        return redirect(url_for('web.notes'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        result = NoteService.update_note(note, title, content)
        
        if result['success']:
            flash('Нотатку успішно оновлено!', 'success')
            return redirect(url_for('web.notes'))
        else:
            flash(result['error'], 'error')
    
    return render_template('note_form.html', mode='edit', note=note)


@web_bp.route('/notes/<int:note_id>/delete', methods=['POST'])
@login_required
def delete_note(note_id):
    """Видалення нотатки"""
    note = NoteService.get_note_by_id(note_id)
    
    if not note:
        flash('Нотатку не знайдено', 'error')
        return redirect(url_for('web.notes'))
    
    # Перевірка прав доступу
    if not NoteService.can_user_modify_note(note, current_user.id, current_user.is_admin()):
        flash('Доступ заборонено', 'error')
        return redirect(url_for('web.notes'))
    
    NoteService.delete_note(note)
    flash('Нотатку успішно видалено!', 'success')
    
    return redirect(url_for('web.notes'))


@web_bp.route('/admin')
@login_required
def admin_panel():
    """Адміністраторська панель (тільки для ADMIN)"""
    if not current_user.is_admin():
        flash('Доступ заборонено. Потрібні права адміністратора.', 'error')
        return redirect(url_for('web.notes'))
    
    users = UserService.get_all_users()
    all_notes = NoteService.get_all_notes()
    stats = NoteService.get_statistics()
    
    return render_template('admin.html', 
                         users=users, 
                         notes=all_notes,
                         total_users=len(users),
                         total_notes=stats['total_notes'])


@web_bp.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    """Видалення користувача (тільки для ADMIN)"""
    if not current_user.is_admin():
        flash('Доступ заборонено', 'error')
        return redirect(url_for('web.notes'))
    
    user = UserService.get_user_by_id(user_id)
    
    if not user:
        flash('Користувача не знайдено', 'error')
        return redirect(url_for('web.admin_panel'))
    
    if user.id == current_user.id:
        flash('Не можна видалити самого себе', 'error')
        return redirect(url_for('web.admin_panel'))
    
    UserService.delete_user(user)
    flash(f'Користувача {user.username} успішно видалено!', 'success')
    
    return redirect(url_for('web.admin_panel'))

