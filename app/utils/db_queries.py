from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.entities.batch import Batch
from app.entities.student import Student
from app.entities.student_batch import StudentBatch
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


# ---------------------- BATCH QUERIES ----------------------:

def get_batch(db: Session, batch_id: int) -> Batch:
    """
        Get batch by id.
    """
    return db.query(Batch).filter(Batch.id == batch_id).first()

def get_all_batches(db: Session) -> List[Batch]:
    """
        Get all batches.
    """
    return db.query(Batch).all()


# ---------------------- STUDENT QUERIES ----------------------:

def get_student_email(db: Session, student_email: int) -> Student:
    """
        Get student email by id.
    """
    return db.query(Student).filter(Student.email == student_email).first()

def get_student(db: Session, student_id: int) -> Student:
    """
        Get student by id.
    """
    return db.query(Student).filter(Student.id == student_id).first()

def get_students(db: Session) -> List[Student]:
    """
        Get all students.
    """
    return db.query(Student).all()

def get_mapped_batch_student(db: Session, mapping_id: int) -> StudentBatch:
    return db.query(StudentBatch).filter(StudentBatch.id == mapping_id).first()

def get_student_in_batch(db: Session, student_id: int, batch_id: int) -> StudentBatch:
    return (
        db.query(StudentBatch)
        .filter(
            StudentBatch.student_id == student_id,
            StudentBatch.batch_id == batch_id
        ).first()
    )