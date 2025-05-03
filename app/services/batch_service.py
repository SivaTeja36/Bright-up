from dataclasses import dataclass
from fastapi import (
    Depends, 
    status,
    HTTPException
)
from pydantic import EmailStr
from sqlalchemy.orm import Session
from automapper import mapper
from app.connectors.database_connector import get_db
from app.entities.user import User
from app.models.user_models import (
    UserCreationRequest, 
    UserCreationResponse,
    GetUserDetailsResponse
)
from app.utils.constants import (
    THE_USER_DETAILS_DOES_NOT_EXIST_FOR_THIS_ID
)


@dataclass
class BatchService:
    db: Session = Depends(get_db)