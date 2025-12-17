from app import db
from app.models.note import Note
from typing import Optional, List


class NoteRepository:
    """Repository для роботи з нотатками в базі даних"""
    
    @staticmethod
    def create(note: Note) -> Note:
        """Створити нову нотатку"""
        db.session.add(note)
        db.session.commit()
        return note
    
    @staticmethod
    def find_by_id(note_id: int) -> Optional[Note]:
        """Знайти нотатку за ID"""
        return Note.query.get(note_id)
    
    @staticmethod
    def find_all() -> List[Note]:
        """Отримати всі нотатки"""
        return Note.query.order_by(Note.created_at.desc()).all()
    
    @staticmethod
    def find_by_user_id(user_id: int) -> List[Note]:
        """Отримати всі нотатки конкретного користувача"""
        return Note.query.filter_by(user_id=user_id).order_by(Note.created_at.desc()).all()
    
    @staticmethod
    def update(note: Note) -> Note:
        """Оновити нотатку"""
        db.session.commit()
        return note
    
    @staticmethod
    def delete(note: Note) -> None:
        """Видалити нотатку"""
        db.session.delete(note)
        db.session.commit()
    
    @staticmethod
    def count_all() -> int:
        """Підрахувати загальну кількість нотаток"""
        return Note.query.count()
    
    @staticmethod
    def count_by_user_id(user_id: int) -> int:
        """Підрахувати кількість нотаток користувача"""
        return Note.query.filter_by(user_id=user_id).count()

