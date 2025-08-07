from pydantic import BaseModel
from typing import (
    Optional,
    TypeVar, 
    Generic
)

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    status_message: str = "SUCCESS"
    data: T


class GetApiResponse(BaseModel, Generic[T]):
    status_message: str = "SUCCESS"
    page: Optional[int] = None
    page_size: Optional[int] = None
    total_items: Optional[int] = None
    data: T


class SuccessMessageResponse(BaseModel):
    id: Optional[int] = None
    message: str