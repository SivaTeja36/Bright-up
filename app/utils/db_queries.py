from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.entities.syllabus import Syllabus
from app.entities.user import User

# ----------------------- USER QUERIES ------------------------:
def get_users(db: Session) -> List[User]:
    """
        Get all users.
    """
    return db.query(User).all()


# ---------------------- SYLLABUS QUERIES ----------------------:

def get_syllabus(db: Session, syllabus_id: int) -> Syllabus:
    """
        Get syllabus by id.
    """
    return db.query(Syllabus).filter(Syllabus.id == syllabus_id).first()

def get_all_syllabus(db: Session) -> List[Syllabus]:
    """
        Get all syllabus.
    """
    return db.query(Syllabus).all()

def get_syllabus_by_name(db: Session, name: str) -> Syllabus:
    """
        Get syllabus by name.
    """
    return db.query(Syllabus).filter(func.lower(Syllabus.name) == name.lower()).first()