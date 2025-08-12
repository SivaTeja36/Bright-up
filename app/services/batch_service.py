from typing import Dict, List

from dataclasses import dataclass
from fastapi import (
    Depends, 
    HTTPException, 
    status
)
from sqlalchemy import func
from sqlalchemy.orm import Session, aliased

from app.connectors.database_connector import get_db
from app.entities.batch import Batch
from app.entities.batch_class_schedule import BatchClassSchedule
from app.entities.batch_mentor import BatchMentor
from app.entities.batch_student import BatchStudent
from app.entities.batch_student_payment import BatchStudentPayment
from app.entities.syllabus import Syllabus
from app.entities.user import User
from app.entities.user_education import UserEducation
from app.models.base_response_models import (
    SuccessMessageResponse,  
    
)
from app.models.batch_models import (
    BatchRequest,
    BatchStudentPaymentRequest, 
    GetBatchResponse,
    GetBatchStudentPayment,
    GetClassScheduleResponse,
    GetMappedBatchStudentResponse,
    MapUserToBatchRequest,
    UpdateClassScheduleRequest,
    UpdatedBatchStudentRequest
)
from app.models.batch_models import ClassScheduleRequest
from app.models.user_models import GetUserDetailsResponse, UserEducationResponse
from app.utils.constants import (
    BATCH_CREATED_SUCCESSFULLY,
    BATCH_DELETED_SUCCESSFULLY,
    BATCH_MENTOR_NOT_FOUND,
    BATCH_NOT_FOUND,
    BATCH_STUDENT_DELETED_SUCCESSFULLY,
    BATCH_STUDENT_NOT_FOUND,
    BATCH_STUDENT_PAYMENT_CREATED_SUCCESSFULLY,
    BATCH_STUDENT_PAYMENT_NOT_FOUND,
    BATCH_STUDENT_PAYMENT_UPDATED_SUCCESSFULLY,
    BATCH_STUDENT_UPDATED_SUCCESSFULLY,
    BATCH_UPDATED_SUCCESSFULLY,
    CLASS_SCHEDULE_CREATED_SUCCESSFULLY,
    CLASS_SCHEDULE_DELETED_SUCCESSFULLY,
    CLASS_SCHEDULE_NOT_FOUND,
    CLASS_SCHEDULE_UPDATED_SUCCESSFULLY,
    ONE_OR_MORE_SYLLABUS_NOT_FOUND,
    REFERRED_USER_NOT_FOUND,
    SCHEDULE_FOR_THIS_DAY_ALREADY_EXISTS_FOR_THIS_BATCH,
    STUDENT_ALREADY_EXISTS_IN_THE_BATCH,
    STUDENT_NOT_FOUND,
    USER_MAPPED_TO_BATCH_SUCCESSFULLY
)
from app.utils.db_queries import (
    count_syllabus_by_ids,
    get_all_batches, 
    get_batch,
    get_batch_class_schedules,
    get_class_schedule_by_batch_and_time,
    get_class_schedule_by_id,
    get_student_in_batch,
    get_user_by_id,
    get_user_education_by_id
)
from app.utils.helpers import get_all_users, get_all_users_dict
from app.utils.validation import (
    validate_data_exits, 
    validate_data_not_found
)


@dataclass
class BatchService:
    db: Session = Depends(get_db)

    def add_batch(self, request: BatchRequest, logged_in_user_id: int) -> Batch:
        new_batch = Batch(
            name=request.name,
            syllabus_ids=list(set(request.syllabus_ids)),
            start_date=request.start_date,
            end_date=request.end_date,
            created_by=logged_in_user_id,
            updated_by=logged_in_user_id
        )
        
        self.db.add(new_batch)
        self.db.commit()

        return new_batch
    
    def add_batch_mentor(
        self, 
        new_batch: Batch, 
        request: BatchRequest, 
        logged_in_user_id: int
    ) -> None:
        batch_mentor = BatchMentor(
            batch_id=new_batch.id,
            mentor_id=request.mentor_id,
            created_by=logged_in_user_id,
            updated_by=logged_in_user_id
        )

        self.db.add(batch_mentor)
        self.db.commit()
      
    
    def create_batch(
        self, 
        request: BatchRequest, 
        logged_in_user_id: int
    ) -> SuccessMessageResponse:
        existing_syllabus_ids = count_syllabus_by_ids(self.db, request.syllabus_ids)
        
        if existing_syllabus_ids != len(request.syllabus_ids):
            validate_data_not_found(False, ONE_OR_MORE_SYLLABUS_NOT_FOUND)
        
        new_batch = self.add_batch(request, logged_in_user_id)
        self.add_batch_mentor(new_batch, request, logged_in_user_id)

        return SuccessMessageResponse(
            message=BATCH_CREATED_SUCCESSFULLY
        )
    
    def get_batch_response(
        self,   
        batch: Batch,    
    ) -> GetBatchResponse:
        users = get_all_users_dict(self.db)
        syllabus_details = self.db.query(Syllabus).filter(Syllabus.id.in_(batch.syllabus_ids)).all()
        mentor = self.db.query(BatchMentor).filter(BatchMentor.batch_id == batch.id).first()
        
        syllabus = [
            {syllabus.name: syllabus.topics}
            for syllabus in syllabus_details
        ]
        
        return GetBatchResponse(
            id=batch.id,
            name=batch.name,
            syllabus=syllabus,
            start_date=batch.start_date,
            end_date=batch.end_date,
            mentor_id=mentor.mentor_id,
            mentor=users.get(mentor.mentor_id),
            created_at=batch.created_at,
            created_by=users.get(batch.created_by),
            updated_at=batch.updated_at,
            updated_by=users.get(batch.updated_by),
            is_active=batch.is_active
        )
        
    def get_all_batches(self) -> list[GetBatchResponse]:
        batches = get_all_batches(self.db)
        
        return [
            self.get_batch_response(batch) for batch in batches
        ]    
    
    def get_batch_by_id(self, batch_id: int) -> GetBatchResponse:
        batch = get_batch(self.db, batch_id)
        validate_data_not_found(batch, BATCH_NOT_FOUND)
       
        return self.get_batch_response(batch)

    def update_batch_by_id(
        self, 
        batch_id: int, 
        request: BatchRequest, 
        logged_in_user_id: int
    ) -> SuccessMessageResponse:
        batch = get_batch(self.db, batch_id)
        validate_data_not_found(batch, BATCH_NOT_FOUND)
        
        existing_syllabus_ids = count_syllabus_by_ids(self.db, request.syllabus_ids)
        
        if existing_syllabus_ids != len(request.syllabus_ids):
            validate_data_not_found(False, ONE_OR_MORE_SYLLABUS_NOT_FOUND)
        
        batch.syllabus_ids = list(set(request.syllabus_ids))
        batch.start_date = request.start_date
        batch.end_date = request.end_date
        batch.updated_at = func.now()
        batch.updated_by = logged_in_user_id
        batch.is_active = request.is_active
            
        self.db.commit()
        
        return SuccessMessageResponse(message=BATCH_UPDATED_SUCCESSFULLY)

    def delete_batch_by_id(self, batch_id: int) -> SuccessMessageResponse:
        batch = get_batch(self.db, batch_id)
        validate_data_not_found(batch, BATCH_NOT_FOUND)
        
        self.db.delete(batch)
        self.db.commit()
        
        return SuccessMessageResponse(message=BATCH_DELETED_SUCCESSFULLY)
    
    def validate_user_details(self, user_details: User, error_message: str):
        if not user_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_message
            )
    
    def create_batch_students(
        self, 
        batch_id: int, 
        request: MapUserToBatchRequest, 
        logged_in_user_id: int
    ) -> SuccessMessageResponse:
        student_user = get_user_by_id(self.db, request.student_id)
        self.validate_user_details(student_user, STUDENT_NOT_FOUND)

        refferal_user = get_user_by_id(self.db, request.referral_by)
        self.validate_user_details(refferal_user, REFERRED_USER_NOT_FOUND)

        batch = get_batch(self.db, batch_id)
        validate_data_not_found(batch, BATCH_NOT_FOUND)
        
        existing_student= get_student_in_batch(self.db, request.student_id, batch_id)
        validate_data_exits(existing_student, STUDENT_ALREADY_EXISTS_IN_THE_BATCH)

        batch_student = BatchStudent(
            batch_id=batch_id,
            student_id=request.student_id,
            class_fee=request.class_fee,
            mentor_fee=request.mentor_fee,
            referral_by=request.referral_by,
            referral_fee=request.referral_fee,
            joined_at=request.joined_at,
            created_by=logged_in_user_id,
            updated_by=logged_in_user_id
        )

        self.db.add(batch_student)
        self.db.commit()

        return SuccessMessageResponse(
            id=batch_student.id,
            message=USER_MAPPED_TO_BATCH_SUCCESSFULLY
        )
    
    def get_batch_student_response(
        self,
        student_user: User,
        student_batch: BatchStudent,
        payments: list[BatchStudentPayment],
        users_dict: dict[int, str]
    ) -> GetMappedBatchStudentResponse:

        paid_fee = sum(p.amount_paid for p in payments)
        mentor_recieved_fee = sum(p.mentor_share for p in payments)
        referral_recieved_fee = sum(p.referral_share for p in payments)

        return GetMappedBatchStudentResponse(
            id=student_batch.id,
            name=student_user.name,
            gender=student_user.gender,
            email=student_user.email,
            phone_number=student_user.phone_number,
            class_fee=student_batch.class_fee,
            paid_fee=paid_fee,
            student_pending_fee=student_batch.class_fee - paid_fee,
            mentor_fee=student_batch.mentor_fee,
            mentor_recieved_fee=mentor_recieved_fee,
            mentor_pending_fee=student_batch.mentor_fee - mentor_recieved_fee,
            referral_by=users_dict.get(student_batch.referral_by),
            referral_fee=student_batch.referral_fee,
            referral_recieved_fee=referral_recieved_fee,
            referral_pending_fee=student_batch.referral_fee - referral_recieved_fee,
            joined_at=student_batch.joined_at,
            created_at=student_batch.created_at,
            created_by=users_dict.get(student_batch.created_by),
            updated_at=student_batch.updated_at,
            updated_by=users_dict.get(student_batch.updated_by)
        )


    def get_batch_students(self, batch_id: int) -> list[GetMappedBatchStudentResponse]:
        batch = get_batch(self.db, batch_id)
        validate_data_not_found(batch, BATCH_NOT_FOUND)

        StudentUser = aliased(User)

        results = (
            self.db.query(StudentUser, BatchStudent)
            .join(StudentUser, StudentUser.id == BatchStudent.student_id)
            .filter(BatchStudent.batch_id == batch_id)
            .all()
        )

        users_dict = get_all_users_dict(self.db)

        batch_student_ids = [bs.id for _, bs in results]
        payments_map = {
            pid: []
            for pid in batch_student_ids
        }
        payments = (
            self.db.query(BatchStudentPayment)
            .filter(BatchStudentPayment.batch_student_id.in_(batch_student_ids))
            .all()
        )

        for p in payments:
            payments_map[p.batch_student_id].append(p)

        return [
            self.get_batch_student_response(student_user, student_batch, payments_map.get(student_batch.id, []), users_dict)
            for student_user, student_batch in results
        ]
    
    def get_batch_student_by_id(self, batch_id: int, batch_student_id: int) -> GetMappedBatchStudentResponse:
        batch = get_batch(self.db, batch_id)
        validate_data_not_found(batch, BATCH_NOT_FOUND)

        StudentUser = aliased(User)

        student_user, student_batch = (
            self.db.query(StudentUser, BatchStudent)
            .join(StudentUser, StudentUser.id == BatchStudent.student_id)
            .filter(
                BatchStudent.batch_id == batch_id,
                BatchStudent.id == batch_student_id
            )
            .first()
        )

        validate_data_not_found(student_batch, BATCH_STUDENT_NOT_FOUND)

        users_dict = get_all_users_dict(self.db)

        payments = (
            self.db.query(BatchStudentPayment)
            .filter(BatchStudentPayment.batch_student_id == student_batch.id)
            .all()
        )

        return self.get_batch_student_response(student_user, student_batch, payments, users_dict)
    
    def update_batch_student_by_id(
        self,
        batch_id: int,
        batch_student_id: int,
        request: UpdatedBatchStudentRequest,
        logged_in_user_id: int
    ) -> SuccessMessageResponse:
        batch = get_batch(self.db, batch_id)
        validate_data_not_found(batch, BATCH_NOT_FOUND)

        student_batch = (
            self.db.query(BatchStudent)
            .filter(
                BatchStudent.batch_id == batch_id,
                BatchStudent.id == batch_student_id
            )
            .first()
        )

        validate_data_not_found(student_batch, BATCH_STUDENT_NOT_FOUND)

        if request.referral_by:
            referred_user = self.db.query(User).filter(User.id == request.referral_by).first()
            validate_data_not_found(referred_user, REFERRED_USER_NOT_FOUND)

        student_batch.class_fee = request.class_fee
        student_batch.mentor_fee = request.mentor_fee
        student_batch.referral_by = request.referral_by
        student_batch.referral_fee = request.referral_fee
        student_batch.joined_at = request.joined_at
        student_batch.updated_at = func.now()
        student_batch.updated_by = logged_in_user_id

        self.db.commit()

        return SuccessMessageResponse(message=BATCH_STUDENT_UPDATED_SUCCESSFULLY)

    def delete_batch_student_by_id(self, batch_id: int, batch_student_id: int) -> SuccessMessageResponse:
        batch = get_batch(self.db, batch_id)
        validate_data_not_found(batch, BATCH_NOT_FOUND)

        batch_student = (
            self.db.query(BatchStudent)
            .filter(
                BatchStudent.batch_id == batch_id,
                BatchStudent.id == batch_student_id
            )
            .first()
        )

        validate_data_not_found(batch_student, BATCH_STUDENT_NOT_FOUND)

        self.db.delete(batch_student)
        self.db.commit() 
        
        return SuccessMessageResponse(message=BATCH_STUDENT_DELETED_SUCCESSFULLY)
    
    def create_batch_student_payment(
        self,
        batch_id: int, 
        batch_student_id: int,
        request: BatchStudentPaymentRequest, 
        logged_in_user_id: int
    ) -> SuccessMessageResponse:
        batch = get_batch(self.db, batch_id)
        validate_data_not_found(batch, BATCH_NOT_FOUND)

        batch_student = (
            self.db.query(BatchStudent)
            .filter(
                BatchStudent.batch_id == batch_id,
                BatchStudent.id == batch_student_id
            )
            .first()
        )

        validate_data_not_found(batch_student, BATCH_STUDENT_NOT_FOUND)

        batch_student_payment = BatchStudentPayment(
            batch_student_id=batch_student_id,
            payment_date=request.payment_date,
            amount_paid=request.amount_paid,
            mentor_share=request.mentor_share,
            referral_share=request.referral_share,
            created_by=logged_in_user_id,
            updated_by=logged_in_user_id
        )

        self.db.add(batch_student_payment)
        self.db.commit()
        
        return SuccessMessageResponse(message=BATCH_STUDENT_PAYMENT_CREATED_SUCCESSFULLY)
    
    def get_all_batch_student_payments(
        self,
        batch_id: int, 
        batch_student_id: int
    ) -> List[GetBatchStudentPayment]:
        batch = get_batch(self.db, batch_id)
        validate_data_not_found(batch, BATCH_NOT_FOUND)

        batch_student = (
            self.db.query(BatchStudent)
            .filter(
                BatchStudent.batch_id == batch_id,
                BatchStudent.id == batch_student_id
            )
            .first()
        )

        validate_data_not_found(batch_student, BATCH_STUDENT_NOT_FOUND)
    
        payments = (
            self.db.query(BatchStudentPayment)
            .filter(BatchStudentPayment.batch_student_id == batch_student_id)
            .all()
        )

        users_dict = get_all_users_dict(self.db)

        return [
            GetBatchStudentPayment(
                id=p.id,
                payment_date=p.payment_date,
                amount_paid=p.amount_paid,
                mentor_share=p.mentor_share,
                referral_share=p.referral_share,
                created_at=p.created_at,
                created_by=users_dict.get(p.created_by),
                updated_at=p.updated_at,
                updated_by=users_dict.get(p.updated_by)
            )
            for p in payments
        ]

    def update_batch_student_payment_by_id(
        self,
        batch_id: int, 
        batch_student_id: int,
        payment_id: int,
        request: BatchStudentPaymentRequest, 
        logged_in_user_id: int
    ) -> SuccessMessageResponse:
        batch = get_batch(self.db, batch_id)
        validate_data_not_found(batch, BATCH_NOT_FOUND)
        
        batch_student = (
            self.db.query(BatchStudent)
            .filter(
                BatchStudent.batch_id == batch_id,
                BatchStudent.id == batch_student_id
            )
            .first()
        )

        validate_data_not_found(batch_student, BATCH_STUDENT_NOT_FOUND)

        payment = (
            self.db.query(BatchStudentPayment)
            .filter(
                BatchStudentPayment.id == payment_id,
                BatchStudentPayment.batch_student_id == batch_student_id
            )
            .first()
        )
        validate_data_not_found(payment, BATCH_STUDENT_PAYMENT_NOT_FOUND)

        payment.payment_date = request.payment_date
        payment.amount_paid = request.amount_paid
        payment.mentor_share = request.mentor_share
        payment.referral_share = request.referral_share
        payment.updated_at = func.now()
        payment.updated_by = logged_in_user_id

        self.db.commit()

        return SuccessMessageResponse(message=BATCH_STUDENT_PAYMENT_UPDATED_SUCCESSFULLY)

    def create_schedule(
        self, 
        batch_id: int, 
        request: ClassScheduleRequest, 
        user_id: int
    ) -> SuccessMessageResponse:
        batch = get_batch(self.db, batch_id)
        validate_data_not_found(batch, BATCH_NOT_FOUND)
        
        existing_class = get_class_schedule_by_batch_and_time(
            self.db, batch_id, 
            request.day, request.start_time
        )
        
        validate_data_exits(
            existing_class, 
            SCHEDULE_FOR_THIS_DAY_ALREADY_EXISTS_FOR_THIS_BATCH
        )

        schedule = BatchClassSchedule(
            batch_id=batch_id,
            day=request.day,
            start_time=request.start_time,
            end_time=request.end_time,
            created_by=user_id,
            updated_by=user_id
        )
        self.db.add(schedule)
        self.db.commit()
        
        return SuccessMessageResponse(message=CLASS_SCHEDULE_CREATED_SUCCESSFULLY)
    
    def get_class_schedule_reponse(self, class_schedule: BatchClassSchedule) -> GetClassScheduleResponse:
        user_dict = get_all_users_dict(self.db)
        
        return GetClassScheduleResponse(
            id=class_schedule.id,
            day=class_schedule.day,
            start_time=class_schedule.start_time,
            end_time=class_schedule.end_time,
            created_at=class_schedule.created_at,
            created_by=user_dict.get(class_schedule.created_by),
            updated_at=class_schedule.updated_at, 
            updated_by=user_dict.get(class_schedule.updated_by),
            is_active=class_schedule.is_active   
        )

    def get_schedules_by_batch(self, batch_id: int) -> List[GetClassScheduleResponse]:
        schedules = get_batch_class_schedules(self.db, batch_id)
        
        return [
            self.get_class_schedule_reponse(class_schedule)
            for class_schedule in schedules
        ]
        
    def validate_update_fields(
        self, 
        schedule: BatchClassSchedule, 
        request: UpdateClassScheduleRequest, 
        batch_id: int
    ) -> None:
        if schedule.day != request.day or schedule.start_time != request.start_time:
            existing_class = get_class_schedule_by_batch_and_time(
                self.db, batch_id, 
                request.day, request.start_time
            )
            
            validate_data_exits(
                existing_class, 
                SCHEDULE_FOR_THIS_DAY_ALREADY_EXISTS_FOR_THIS_BATCH
            )    

    def update_schedule_by_id(
        self, 
        schedule_id: int,
        batch_id: int, 
        request: UpdateClassScheduleRequest, 
        user_id: int
    ) -> SuccessMessageResponse:
        batch = get_batch(self.db, batch_id)
        validate_data_not_found(batch, BATCH_NOT_FOUND)
        
        schedule = get_class_schedule_by_id(self.db, schedule_id, batch_id)
        validate_data_not_found(schedule, CLASS_SCHEDULE_NOT_FOUND)

        self.validate_update_fields(schedule, request, schedule.batch_id)

        schedule.day = request.day
        schedule.start_time = request.start_time
        schedule.end_time = request.end_time
        schedule.updated_by = user_id

        self.db.commit()
        
        return SuccessMessageResponse(message=CLASS_SCHEDULE_UPDATED_SUCCESSFULLY)

    def delete_schedule_by_id(self, schedule_id: int, batch_id: int) -> SuccessMessageResponse:
        batch = get_batch(self.db, batch_id)
        validate_data_not_found(batch, BATCH_NOT_FOUND)

        schedule = get_class_schedule_by_id(self.db, schedule_id, batch_id)
        validate_data_not_found(schedule, CLASS_SCHEDULE_NOT_FOUND)

        self.db.delete(schedule)
        self.db.commit()
        
        return SuccessMessageResponse(message=CLASS_SCHEDULE_DELETED_SUCCESSFULLY)