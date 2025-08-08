from datetime import datetime
from typing import Optional
from pydantic import (
    BaseModel, 
    EmailStr,
    field_validator
)

from app.utils.validation import validate_password

class UserCreationRequest(BaseModel):
    name: str
    email: EmailStr
    gender: str
    password: str
    role: str
    phone_number: str

    @field_validator("password")
    def validate_user_creation_password(cls, password: str):
        return validate_password(password)


class UserResponse(BaseModel):
    id: int
    message: str


class GetUserDetailsResponse(BaseModel):
    id: int
    name: str 
    email: str 
    gender: str
    phone_number: str
    role: str
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
        