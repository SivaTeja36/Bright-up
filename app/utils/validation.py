from typing import Any

from fastapi import (
    HTTPException,
    status
)


def validate_data_not_found(data: Any, error_message: str) -> None:
    if not data:
        raise HTTPException(    
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_message,
        )  
        
        
def validate_data_exits(data: Any, error_message: str) -> None:
    if data:
        raise HTTPException(    
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message,
        )      