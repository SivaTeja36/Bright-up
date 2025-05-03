from dataclasses import dataclass
from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.connectors.database_connector import get_db
from app.entities.batch import Batch
from app.models.base_response_model import SuccessMessageResponse
from app.models.batch_models import (
    BatchRequest, 
    GetBatchResponse
)
from app.utils.constants import (
    BATCH_CREATED_SUCCESSFULLY,
    BATCH_DELETED_SUCCESSFULLY,
    BATCH_NOT_FOUND,
    BATCH_UPDATED_SUCCESSFULLY
)
from app.utils.db_queries import get_all_batches, get_batch
from app.utils.helpers import get_all_users_dict
from app.utils.validation import validate_data_exists


@dataclass
class BatchService:
    db: Session = Depends(get_db)
    
    def create_batch(
        self, 
        request: BatchRequest, 
        logged_in_user_id: int
    ) -> SuccessMessageResponse:
        new_batch = Batch(
            syllabus_ids=request.syllabus_ids,
            start_date=request.start_date,
            end_date=request.end_date,
            created_by=logged_in_user_id,
            updated_by=logged_in_user_id
        )
        
        self.db.add(new_batch)
        self.db.commit()
      
        return SuccessMessageResponse(
            message=BATCH_CREATED_SUCCESSFULLY
        )
    
    def get_batch_response(
        self,   
        batch: Batch,    
    ) -> GetBatchResponse:
        users = get_all_users_dict(self.db)
        
        return GetBatchResponse(
            id=batch.id,
            syllabus_ids=batch.syllabus_ids,
            start_date=batch.start_date,
            end_date=batch.end_date,
            created_at=batch.created_at,
            created_by=users.get(batch.created_by),
            updated_at=batch.updated_at,
            updated_by=users.get(batch.updated_by),
            is_active=batch.is_active
        )
        
    def get_all_batches(self) -> list[GetBatchResponse]:
        batches = get_all_batches(self.db)
        
        return [
            self.get_batch_response(batch) for batch in batches
        ]    
    
    def get_batch_by_id(self, batch_id: int) -> GetBatchResponse:
        batch = get_batch(self.db, batch_id)
        validate_data_exists(batch, BATCH_NOT_FOUND)
       
        return self.get_batch_response(batch)

    def update_batch(
        self, 
        batch_id: int, 
        request: BatchRequest, 
        logged_in_user_id: int
    ) -> SuccessMessageResponse:
        batch = get_batch(self.db, batch_id)
        validate_data_exists(batch, BATCH_NOT_FOUND)
        
        batch.syllabus_ids = request.syllabus_ids
        batch.start_date = request.start_date
        batch.end_date = request.end_date
        batch.updated_at = func.now()
        batch.updated_by = logged_in_user_id
        batch.is_active = request.is_active
            
        self.db.commit()
        
        return SuccessMessageResponse(message=BATCH_UPDATED_SUCCESSFULLY)

    def delete_batch(self, batch_id: int) -> SuccessMessageResponse:
        batch = get_batch(self.db, batch_id)
        validate_data_exists(batch, BATCH_NOT_FOUND)
        
        self.db.delete(batch)
        self.db.commit()
        
        return SuccessMessageResponse(message=BATCH_DELETED_SUCCESSFULLY)