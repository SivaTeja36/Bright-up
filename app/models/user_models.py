from datetime import datetime
from typing import Optional
from pydantic import (
    BaseModel, 
    EmailStr,
    field_validator
)

from app.utils.enums import UserEducationStatus
from app.utils.validation import validate_password

class UserEducationRequest(BaseModel):
    degree: str
    specialization: str 
    start_year: int
    end_year: int
    current_year_of_study: Optional[int] = None
    status: UserEducationStatus
    city: str 
    state: str 


class UserCreationRequest(BaseModel):
    name: str
    email: EmailStr
    gender: str
    password: str
    role: str
    phone_number: str
    education: UserEducationRequest

    @field_validator("password")
    def validate_user_creation_password(cls, password: str):
        return validate_password(password)


class UserResponse(BaseModel):
    id: int
    message: str


class UserEducationResponse(BaseModel):
    id: int 
    degree: str 
    specialization: str 
    start_year: int 
    end_year: int 
    current_year_of_study: Optional[int] = None
    status: str 
    city: str 
    state: str 
    created_at: datetime 
    created_by: str 
    updated_at: datetime
    updated_by: str


class GetUserDetailsResponse(BaseModel):
    id: int
    name: str 
    email: str 
    gender: str
    phone_number: str
    role: str
    education: UserEducationResponse
    created_at: datetime
    created_by: Optional[str] = None
    updated_at: datetime
    updated_by: Optional[str] = None
    is_active: bool


class UpdateUserRequest(BaseModel):
    name: str
    gender: str
    role: str
    phone_number: str
    education: UserEducationRequest
    is_active: Optional[bool] = None


class UpdateUserPassword(BaseModel):
    password: str

    @field_validator("password")
    def validate_user_creation_password(cls, password: str):
        return validate_password(password)


class CurrentContextUser:
    id: int
    name: str
    email: str
    role: str


class UserInfoResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
        