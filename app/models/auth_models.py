
from pydantic import (
    BaseModel, 
    EmailStr,
    field_validator
)

from app.utils.validation import validate_password


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_user_creation_password(cls, password: str):
        return validate_password(password)


class LoginResponse(BaseModel):
    token: str