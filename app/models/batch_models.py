from datetime import (
    date, 
    datetime,
    time
)
from typing import (
    Optional, 
    List
)

from pydantic import BaseModel, PositiveInt

from app.utils.enums import Days


class BatchRequest(BaseModel):
    name: str
    syllabus_ids: Optional[List[int]] = None
    start_date: date
    end_date: date
    mentor_id: int
    is_active: Optional[bool] = True
    

class GetBatchResponse(BaseModel):
    id: int 
    name: str
    syllabus: List[dict] = None
    start_date: date
    end_date: date
    mentor: str
    created_at: datetime 
    created_by: str
    updated_at: datetime 
    updated_by: str
    is_active: bool 


class MapUserToBatchRequest(BaseModel):
    student_id: PositiveInt 
    class_fee: PositiveInt
    mentor_fee: PositiveInt
    referral_by: PositiveInt
    referral_fee: PositiveInt
    joined_at: date 
    

class GetMappedBatchStudentResponse(BaseModel):
    id: int
    name: str
    gender: str
    email: str
    phone_number: str
    class_fee: int 
    paid_fee: int
    student_pending_fee: int 
    mentor_fee: int
    mentor_recieved_fee: int
    mentor_pending_fee: int
    referral_by: str
    referral_fee: float
    referral_recieved_fee: int
    referral_pending_fee: int
    joined_at: date 
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str


class UpdatedBatchStudentRequest(BaseModel):
    class_fee: PositiveInt
    mentor_fee: PositiveInt
    referral_by: PositiveInt
    referral_fee: PositiveInt
    joined_at: date 
    

class ClassScheduleRequest(BaseModel):
    day: Days
    start_time: time 
    end_time: time
    
    
class GetClassScheduleResponse(BaseModel):
    id: int 
    day: str 
    start_time: time 
    end_time: time
    created_at: datetime 
    created_by: str
    updated_at: datetime 
    updated_by: str
    is_active: bool    
    
    
class UpdateClassScheduleRequest(BaseModel):
    day: Days
    start_time: time
    end_time: time