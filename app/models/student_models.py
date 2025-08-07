from datetime import date, datetime
from typing import Optional

from pydantic import (
    BaseModel, 
    EmailStr
)


class StudentRequest(BaseModel):
    user_id: int
    degree: str 
    specialization: str 
    passout_year: int
    city: str 
    state: str
    referral_by: int 
    

class GetStudentResponse(BaseModel):
    id: int 
    name: str
    degree: str 
    specialization: str
    passout_year: int 
    city: str
    state: str
    referral_by: str 
    created_at: datetime 
    created_by: str
    updated_at: datetime 
    updated_by: str
    is_active: bool 
    

class MapStudentToBatchRequest(BaseModel):
    batch_id: int 
    class_amount: int 
    amount_paid: int
    mentor_amount: int 
    referral_by: int 
    referral_percentage: float 
    referral_amount: int
    joined_at: date
    

class GetMappedBatchStudentResponse(BaseModel):
    id: int
    name: str
    gender: str
    email: str
    phone_number: str
    class_amount: int 
    mentor_amount: int
    balance_amount: Optional[int] = None
    referral_by: str
    referral_percentage: float
    referral_amount: int
    joined_at: date 
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    
 
class UpdatedBatchStudentRequest(BaseModel):
    amount: int
    joined_at: date   