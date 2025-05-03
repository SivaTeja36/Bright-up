from pydantic import BaseModel
from typing import (
    TypeVar, 
    Generic
)

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    status_message: str = "SUCCESS"
    data: T


class SuccessMessageResponse(BaseModel):
    message: str