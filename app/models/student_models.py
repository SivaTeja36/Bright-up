from datetime import date, datetime

from pydantic import (
    BaseModel, 
    EmailStr
)


class StudentRequest(BaseModel):
    name: str
    gender: str 
    email: str
    phone_number: str
    degree: str 
    specialization: str 
    passout_year: int 
    city: str 
    state: str 
    refered_by: str
    

class GetStudentResponse(BaseModel):
    id: int 
    name: str 
    gender: str
    email: EmailStr 
    phone_number: str 
    degree: str 
    specialization: str 
    passout_year: int 
    city: str 
    state: str
    refered_by: str 
    created_at: datetime 
    created_by: int 
    updated_at: datetime 
    updated_by: int 
    is_active: bool
    

class MapStudentToBatchRequest(BaseModel):
    batch_id: int 
    amount: int 
    joined_at: date
    

class GetMappedBatchStudentResponse(BaseModel):
    name: str
    gender: str
    email: str
    phone_number: str
    amount: int 
    joined_at: date 
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    
 
class UpdatedBatchStudentRequest(BaseModel):
    amount: int
    joined_at: date   