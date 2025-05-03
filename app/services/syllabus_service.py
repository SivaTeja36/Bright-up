from dataclasses import dataclass
from fastapi import (
    Depends, 
    status,
    HTTPException
)
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.connectors.database_connector import get_db
from app.entities.syllabus import Syllabus
from app.models.base_response_model import SuccessMessageResponse
from app.models.syllabus_models import (
    GetSyllabusResponse, 
    SyllabusRequest
)
from app.utils.constants import (
    SYLLABUS_CREATED_SUCCESSFULLY,
    SYLLABUS_DELETED_SUCCESSFULLY,
    SYLLABUS_NAME_ALREADY_EXISTS,
    SYLLABUS_NOT_FOUND
)
from app.utils.db_queries import (
    get_all_syllabus,
    get_syllabus, 
    get_syllabus_by_name
)
from app.utils.helpers import get_all_users_dict
from app.utils.validation import validate_data_exits, validate_data_not_found


@dataclass
class SyllabusService:
    db: Session = Depends(get_db)
    
    def create_syllabus(
        self, 
        request: SyllabusRequest, 
        logged_in_user_id: int
    ) -> SuccessMessageResponse:
        existing_syllabus = get_syllabus_by_name(self.db, request.name)
        validate_data_exits(existing_syllabus, SYLLABUS_NAME_ALREADY_EXISTS)
        
        syllabus = Syllabus(
            name=request.name,
            topics=list(set(request.topics)),
            created_by=logged_in_user_id,
            updated_by=logged_in_user_id
        )
        
        self.db.add(syllabus)
        self.db.commit()
        
        return SuccessMessageResponse(
            message=SYLLABUS_CREATED_SUCCESSFULLY
        )
        
    def get_syllabus_response(
        self,   
        syllabus: Syllabus,    
    ) -> GetSyllabusResponse:  
        users = get_all_users_dict(self.db)
        
        return GetSyllabusResponse(
            id=syllabus.id,
            name=syllabus.name,
            topics=syllabus.topics,
            created_at=syllabus.created_at,
            created_by=users.get(syllabus.created_by),
            updated_at=syllabus.updated_at,
            updated_by=users.get(syllabus.updated_by)
        )
        
    def get_all_syllabus(self) -> list[GetSyllabusResponse]:
        syllabus_list = get_all_syllabus(self.db)
        
        return [
            self.get_syllabus_response(syllabus)
            for syllabus in syllabus_list
        ]    
        
    def get_syllabus_by_id(self, syllabus_id: int) -> Syllabus:
        syllabus = get_syllabus(self.db, syllabus_id)
        validate_data_not_found(syllabus, SYLLABUS_NOT_FOUND)
            
        return self.get_syllabus_response(syllabus)
    
    def validate_update_fields(
        self, 
        syllabus: Syllabus, 
        request: SyllabusRequest
    ) -> None:
        if syllabus.name != request.name:
            existing_syllabus = get_syllabus_by_name(self.db, request.name)
            validate_data_exits(existing_syllabus, SYLLABUS_NAME_ALREADY_EXISTS)
        
    def update_syllabus_by_id(
        self, 
        syllabus_id: int, 
        request: SyllabusRequest, 
        logged_in_user_id: int
    ) -> SuccessMessageResponse:
        syllabus = get_syllabus(self.db, syllabus_id)
        validate_data_not_found(syllabus, SYLLABUS_NOT_FOUND)
        self.validate_update_fields(syllabus, request)
        
        syllabus.name = request.name
        syllabus.topics = list(set(request.topics))
        syllabus.updated_at = func.now()
        syllabus.updated_by = logged_in_user_id
        
        self.db.commit()
        
        return SuccessMessageResponse(
            message=SYLLABUS_CREATED_SUCCESSFULLY
        )     
        
    def delete_syllabus_by_id(
        self, 
        syllabus_id: int
    ) -> SuccessMessageResponse:
        syllabus = get_syllabus(self.db, syllabus_id)
        validate_data_not_found(syllabus, SYLLABUS_NOT_FOUND)
        
        self.db.delete(syllabus)
        self.db.commit()
        
        return SuccessMessageResponse(
            message=SYLLABUS_DELETED_SUCCESSFULLY
        )    