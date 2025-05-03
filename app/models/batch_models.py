from datetime import (
    date, 
    datetime
)
from typing import (
    Optional, 
    List
)

from pydantic import BaseModel


class BatchRequest(BaseModel):
    syllabus_ids: Optional[List[int]] = None
    start_date: date
    end_date: date
    mentor_name: str
    is_active: Optional[bool] = True
    

class GetBatchResponse(BaseModel):
    id: int 
    syllabus: List[dict] = None
    start_date: date
    end_date: date
    mentor_name: str
    created_at: datetime 
    created_by: str
    updated_at: datetime 
    updated_by: int
    is_active: bool 