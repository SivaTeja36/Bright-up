from datetime import datetime
from pydantic import (
    BaseModel, 
    EmailStr
)

class UserCreationRequest(BaseModel):
    name: str
    username: EmailStr
    password: str
    role: str
    contact: str


class UserCreationResponse(BaseModel):
    id: int
    name: str 
    username: str 
    contact: str
    role: str
    created_at: datetime
    is_active: bool


class GetUserDetailsResponse(BaseModel):
    id: int
    name: str 
    username: str 
    contact: str
    role: str
    created_at: datetime
    is_active: bool


class CurrentContextUser():
    user_id: int
    username: str
    name: str
    role: str