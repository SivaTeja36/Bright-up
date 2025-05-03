from datetime import datetime
from typing import List

from pydantic import BaseModel


class SyllabusRequest(BaseModel):
    name: str
    topics: List[str]
    

class GetSyllabusResponse(BaseModel):
    id: int
    name: str 
    topics: List[str]
    created_at: datetime
    created_by: str 
    updated_at: datetime 
    updated_by: str 