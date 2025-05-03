from dataclasses import dataclass
from typing import List

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.connectors.database_connector import get_db
from app.entities.student import Student
from app.entities.student_batch import StudentBatch
from app.models.base_response_model import SuccessMessageResponse
from app.models.student_models import (
    GetMappedBatchStudentResponse,
    GetStudentResponse,
    MapStudentToBatchRequest, 
    StudentRequest,
    UpdatedBatchStudentRequest
)
from app.utils.constants import (
    MAPPING_NOT_FOUND,
    STUDENT_ALREADY_EXISTS_IN_THE_BATCH,
    STUDENT_BATCH_DETAILS_CREATED_SUCCESSFULLY,
    STUDENT_BATCH_DETAILS_DELETED_SUCCESSFULLY,
    STUDENT_BATCH_DETAILS_UPDATED_SUCCESSFULLY,
    STUDENT_CREATED_SUCCESSFULLY,
    STUDENT_DELETED_SUCCESSFULLY,
    STUDENT_EMAIL_ALREADY_EXISTS,
    STUDENT_NOT_FOUND,
    STUDENT_UPDATED_SUCCESSFULLY
)
from app.utils.db_queries import (
    get_mapped_batch_student,
    get_student, 
    get_student_email,
    get_student_in_batch,
    get_students
)
from app.utils.helpers import get_all_users_dict
from app.utils.validation import validate_data_not_found


@dataclass
class StudentService:
    db: Session = Depends(get_db)

    def create_student(
        self, 
        request: StudentRequest, 
        logged_in_user_id: int
    ) -> SuccessMessageResponse:
        existing_email = get_student_email(self.db, request.email)
        validate_data_not_found(existing_email, STUDENT_EMAIL_ALREADY_EXISTS)

        new_student = Student(
            name=request.name,
            gender=request.gender,
            email=request.email,
            phone_number=request.phone_number,
            degree=request.degree,
            specialization=request.specialization,
            passout_year=request.passout_year,
            city=request.city,
            state=request.state,
            refered_by=request.refered_by,
            created_by=logged_in_user_id,
            updated_by=logged_in_user_id
        )
        self.db.add(new_student)
        self.db.commit()

        return SuccessMessageResponse(message=STUDENT_CREATED_SUCCESSFULLY)
    
    def get_student_response(self, student: Student) -> GetStudentResponse:
        users = get_all_users_dict(self.db)
        
        return GetStudentResponse(
            id=student.id,
            name=student.name,
            gender=student.gender,
            email=student.email,
            phone_number=student.phone_number,
            degree=student.degree,
            specialization=student.specialization,
            passout_year=student.passout_year,
            city=student.city,
            state=student.state,
            refered_by=student.refered_by,
            created_at=student.created_at,
            created_by=users.get(student.created_by),
            updated_at=student.updated_at,
            updated_by=users.get(student.updated_by),
            is_active=student.is_active
        )
        
    def get_all_students(self) -> List[GetStudentResponse]:
        students = get_students(self.db)  
        
        return [
            self.get_student_response(student)
            for student in students
        ]
        
    def get_student_by_id(self, student_id: int) -> GetStudentResponse:
        student = get_student(self.db, student_id)
        validate_data_not_found(student, STUDENT_NOT_FOUND)

        return self.get_student_response(student)

    def update_student_by_id(
        self, 
        student_id: int, 
        request: StudentRequest,
        logged_in_user_id: int
    ) -> GetStudentResponse:
        student = get_student(self.db, student_id)
        validate_data_not_found(student, STUDENT_NOT_FOUND)

        for key, value in request.dict().items():
            setattr(student, key, value)
            
        student.updated_at = func.now()
        student.updated_by = logged_in_user_id    

        self.db.commit()

        return SuccessMessageResponse(message=STUDENT_UPDATED_SUCCESSFULLY)

    def delete_student_by_id(self, student_id: int) -> None:
        student = get_student(self.db, student_id)
        validate_data_not_found(student, STUDENT_NOT_FOUND)

        self.db.delete(student)
        self.db.commit()
        
        return SuccessMessageResponse(message=STUDENT_DELETED_SUCCESSFULLY)
    
    def map_student_to_batch(
        self,
        student_id: int,
        request: MapStudentToBatchRequest,
        logged_in_user_id: int
    ) -> SuccessMessageResponse:
        student = get_student(self.db, student_id)
        validate_data_not_found(student, STUDENT_NOT_FOUND)
        
        existing_student= get_student_in_batch(self.db, student_id, request.batch_id)
        validate_data_not_found(existing_student, STUDENT_ALREADY_EXISTS_IN_THE_BATCH)

        student_batch = StudentBatch(
            student_id=student_id,
            batch_id=request.batch_id,
            amount=request.amount,
            joined_at=request.joined_at,
            created_by=logged_in_user_id,
            updated_by=logged_in_user_id
        )

        self.db.add(student_batch)
        self.db.commit()

        return SuccessMessageResponse(message=STUDENT_BATCH_DETAILS_CREATED_SUCCESSFULLY)
    
    def get_batch_student_response(
        self, 
        student: Student, 
        student_batch: StudentBatch
    ) -> GetMappedBatchStudentResponse:
        users_dict = get_all_users_dict(self.db)
        
        return GetMappedBatchStudentResponse(
            name=student.name,
            gender=student.gender,
            email=student.email,
            phone_number=student.phone_number,
            amount=student_batch.amount,
            joined_at=student_batch.joined_at,
            created_at=student_batch.created_at,
            created_by=users_dict.get(student_batch.created_by),
            updated_at=student_batch.updated_at,
            updated_by=users_dict.get(student_batch.updated_by)
        )

    def get_batch_students(self, batch_id: int) -> List[GetMappedBatchStudentResponse]:
        results = (
            self.db.query(Student, StudentBatch)
            .join(StudentBatch, Student.id == StudentBatch.student_id)
            .filter(StudentBatch.batch_id == batch_id)
            .all()
        )

        return [
            self.get_batch_student_response(student, student_batch)
            for student, student_batch in results
        ]

    def get_batch_student_by_id(self, mapping_id: int) -> SuccessMessageResponse:
        student_batch = get_mapped_batch_student(self.db, mapping_id)
        validate_data_not_found(student_batch, MAPPING_NOT_FOUND)
        student = get_student(self.db, student_batch.student_id)

        return self.get_batch_student_response(student, student_batch)

    def update_batch_student_by_id(
        self,
        mapping_id: int,
        request: UpdatedBatchStudentRequest,
        logged_in_user_id: int
    ) -> SuccessMessageResponse:
        student_batch = get_mapped_batch_student(self.db, mapping_id)
        validate_data_not_found(student_batch, MAPPING_NOT_FOUND)

        student_batch.amount = request.amount
        student_batch.joined_at = request.joined_at
        student_batch.updated_at = func.now()
        student_batch.updated_by = logged_in_user_id

        self.db.commit()

        return SuccessMessageResponse(message=STUDENT_BATCH_DETAILS_UPDATED_SUCCESSFULLY)

    def delete_batch_student_by_id(self, mapping_id: int) -> SuccessMessageResponse:
        student_batch = get_mapped_batch_student(self.db, mapping_id)
        validate_data_not_found(student_batch, MAPPING_NOT_FOUND)

        self.db.delete(student_batch)
        self.db.commit() 
        
        return SuccessMessageResponse(message=STUDENT_BATCH_DETAILS_DELETED_SUCCESSFULLY)