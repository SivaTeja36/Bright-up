from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.entities.batch import Batch
from app.entities.class_schedule import ClassSchedule
from app.entities.student import Student
from app.entities.batch_student import BatchStudent
from app.entities.syllabus import Syllabus
from app.entities.user import User

# ----------------------- USER QUERIES ------------------------:
def get_users(db: Session) -> List[User]:
    """
        Get all users.
    """
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    return (
        db.query(User)
        .filter(
            User.id == user_id
        ).first()
    )

def get_user_by_email(db: Session, email: str):
    return (
        db.query(User)
        .filter(
            func.lower(User.email) == email.lower()
        ).first()
    )

def get_user_by_phone_number(db: Session, phone_number: str):
    return (
        db.query(User)
        .filter(
            User.phone_number == phone_number
        ).first()
    )

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

def count_syllabus_by_ids(db: Session, syllabus_ids: List[int]) -> int:
    """
        Count the number of syllabus entries matching the given IDs.
    """
    return db.query(func.count(Syllabus.id)).filter(Syllabus.id.in_(syllabus_ids)).scalar()

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

def get_batch_class_schedules(db: Session, batch_id: int):
    return db.query(ClassSchedule).filter_by(batch_id=batch_id, is_active=True).all()

def get_class_schedule_by_batch_and_time(db: Session, batch_id: int, day: str, start_time: str) -> ClassSchedule:
    """
        Get class schedule by batch ID, day, and start time.
    """
    return db.query(ClassSchedule).filter_by(
        batch_id=batch_id,
        day=day,
        start_time=start_time,
        is_active=True
    ).first()
    
def get_class_schedule_by_id(db: Session, schedule_id: int) -> ClassSchedule:
    """
        Get class schedule by ID.
    """
    return db.query(ClassSchedule).filter_by(id=schedule_id, is_active=True).first()


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

def get_mapped_batch_student(db: Session, mapping_id: int) -> BatchStudent:
    return db.query(BatchStudent).filter(BatchStudent.id == mapping_id).first()

def get_student_in_batch(db: Session, student_id: int, batch_id: int) -> BatchStudent:
    return (
        db.query(BatchStudent)
        .filter(
            BatchStudent.student_id == student_id,
            BatchStudent.batch_id == batch_id
        ).first()
    )
    
    