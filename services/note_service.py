from app.models.note import Note
from app.repositories.note_repository import NoteRepository
from typing import Optional, List, Dict


class NoteService:
    """Service для бізнес-логіки роботи з нотатками"""
    
    @staticmethod
    def create_note(title: str, content: str, user_id: int) -> Dict:
        """Створити нову нотатку з валідацією"""
        
        # Валідація
        if not title or len(title.strip()) == 0:
            return {'success': False, 'error': 'Заголовок не може бути порожнім'}
        
        if len(title) > 200:
            return {'success': False, 'error': 'Заголовок не може перевищувати 200 символів'}
        
        if not content or len(content.strip()) == 0:
            return {'success': False, 'error': 'Вміст не може бути порожнім'}
        
        # Створення нотатки
        note = Note(
            title=title.strip(),
            content=content.strip(),
            user_id=user_id
        )
        
        created_note = NoteRepository.create(note)
        return {'success': True, 'note': created_note}
    
    @staticmethod
    def get_note_by_id(note_id: int) -> Optional[Note]:
        """Отримати нотатку за ID"""
        return NoteRepository.find_by_id(note_id)
    
    @staticmethod
    def get_all_notes() -> List[Note]:
        """Отримати всі нотатки"""
        return NoteRepository.find_all()
    
    @staticmethod
    def get_notes_by_user(user_id: int) -> List[Note]:
        """Отримати нотатки конкретного користувача"""
        return NoteRepository.find_by_user_id(user_id)
    
    @staticmethod
    def update_note(note: Note, title: str = None, content: str = None) -> Dict:
        """Оновити нотатку"""
        
        if title is not None:
            if len(title.strip()) == 0:
                return {'success': False, 'error': 'Заголовок не може бути порожнім'}
            if len(title) > 200:
                return {'success': False, 'error': 'Заголовок не може перевищувати 200 символів'}
            note.title = title.strip()
        
        if content is not None:
            if len(content.strip()) == 0:
                return {'success': False, 'error': 'Вміст не може бути порожнім'}
            note.content = content.strip()
        
        updated_note = NoteRepository.update(note)
        return {'success': True, 'note': updated_note}
    
    @staticmethod
    def delete_note(note: Note) -> None:
        """Видалити нотатку"""
        NoteRepository.delete(note)
    
    @staticmethod
    def can_user_modify_note(note: Note, user_id: int, is_admin: bool = False) -> bool:
        """Перевірити чи може користувач модифікувати нотатку"""
        # Адміністратор може модифікувати будь-яку нотатку
        # Звичайний користувач може модифікувати тільки свої нотатки
        return is_admin or note.user_id == user_id
    
    @staticmethod
    def get_statistics() -> Dict:
        """Отримати статистику по нотатках"""
        return {
            'total_notes': NoteRepository.count_all()
        }

