from typing import List

from dataclasses import dataclass
from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.connectors.database_connector import get_db
from app.entities.batch import Batch
from app.entities.class_schedule import ClassSchedule
from app.models.base_response_model import (
    SuccessMessageResponse,  
    
)
from app.models.batch_models import (
    BatchRequest, 
    GetBatchResponse,
    GetClassScheduleResponse,
    UpdateClassScheduleRequest
)
from app.models.batch_models import ClassScheduleRequest
from app.utils.constants import (
    BATCH_CREATED_SUCCESSFULLY,
    BATCH_DELETED_SUCCESSFULLY,
    BATCH_NOT_FOUND,
    BATCH_UPDATED_SUCCESSFULLY,
    CLASS_SCHEDULE_CREATED_SUCCESSFULLY,
    CLASS_SCHEDULE_DELETED_SUCCESSFULLY,
    CLASS_SCHEDULE_NOT_FOUND,
    CLASS_SCHEDULE_UPDATED_SUCCESSFULLY,
    SCHEDULE_FOR_THIS_DAY_ALREADY_EXISTS_FOR_THIS_BATCH
)
from app.utils.db_queries import (
    get_all_batches, 
    get_batch,
    get_batch_class_schedules
)
from app.utils.helpers import get_all_users_dict
from app.utils.validation import validate_data_not_found


@dataclass
class BatchService:
    db: Session = Depends(get_db)
    
    def create_batch(
        self, 
        request: BatchRequest, 
        logged_in_user_id: int
    ) -> SuccessMessageResponse:
        new_batch = Batch(
            syllabus_ids=request.syllabus_ids,
            start_date=request.start_date,
            end_date=request.end_date,
            mentor_name=request.mentor_name,
            created_by=logged_in_user_id,
            updated_by=logged_in_user_id
        )
        
        self.db.add(new_batch)
        self.db.commit()
      
        return SuccessMessageResponse(
            message=BATCH_CREATED_SUCCESSFULLY
        )
    
    def get_batch_response(
        self,   
        batch: Batch,    
    ) -> GetBatchResponse:
        users = get_all_users_dict(self.db)
        
        return GetBatchResponse(
            id=batch.id,
            syllabus_ids=batch.syllabus_ids,
            start_date=batch.start_date,
            end_date=batch.end_date,
            mentor_name=batch.mentor_name,
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
        
        batch.syllabus_ids = request.syllabus_ids
        batch.start_date = request.start_date
        batch.end_date = request.end_date
        batch.mentor_name = request.mentor_name
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
    
    def create_schedule(
        self, batch_id: int, request: ClassScheduleRequest, user_id: int
    ) -> SuccessMessageResponse:
        existing_class = self.db.query(ClassSchedule).filter_by(
            batch_id=batch_id,
            day=request.day,
            start_time=request.start_time,
            is_active=True
        ).first()
        
        validate_data_not_found(existing_class, SCHEDULE_FOR_THIS_DAY_ALREADY_EXISTS_FOR_THIS_BATCH, 400)

        schedule = ClassSchedule(
            batch_id=batch_id,
            day=request.day.value,
            start_time=request.start_time,
            end_time=request.end_time,
            created_by=user_id,
            updated_by=user_id
        )
        self.db.add(schedule)
        self.db.commit()
        
        return SuccessMessageResponse(message=CLASS_SCHEDULE_CREATED_SUCCESSFULLY)
    
    def get_class_schedule_reponse(self, class_schedule: ClassSchedule):
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

    def update_schedule_by_id(
        self, schedule_id: int, request: UpdateClassScheduleRequest, user_id: int
    ) -> SuccessMessageResponse:
        schedule = self.db.query(ClassSchedule).filter_by(id=schedule_id, is_active=True).first()
        validate_data_not_found(schedule, CLASS_SCHEDULE_NOT_FOUND)

        schedule.day = request.day.value
        schedule.start_time = request.start_time
        schedule.end_time = request.end_time
        schedule.updated_by = user_id

        self.db.commit()
        return SuccessMessageResponse(message=CLASS_SCHEDULE_UPDATED_SUCCESSFULLY)

    def delete_schedule_by_id(self, schedule_id: int) -> SuccessMessageResponse:
        schedule = self.db.query(ClassSchedule).filter_by(id=schedule_id, is_active=True).first()
        validate_data_not_found(schedule, CLASS_SCHEDULE_NOT_FOUND)

        schedule.is_active = False
        self.db.commit()
        return SuccessMessageResponse(message=CLASS_SCHEDULE_DELETED_SUCCESSFULLY)