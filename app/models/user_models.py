from datetime import datetime
from typing import Optional
from pydantic import (
    BaseModel, 
    EmailStr
)

class UserCreationRequest(BaseModel):
    name: str
    email: EmailStr
    gender: str
    password: str
    role: str
    phone_number: str


class UserCreationResponse(BaseModel):
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


class CurrentContextUser():
    id: int
    name: str
    email: str
    role: str