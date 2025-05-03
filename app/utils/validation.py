from typing import Any

from fastapi import (
    HTTPException,
    status
)


def validate_data_not_found(data: Any, error_message: str, status_code: int = 404) -> None:
    if not data:
        raise HTTPException(    
            status_code=status_code,
            detail=error_message,
        )  
        
        
def validate_data_exits(data: Any, error_message: str) -> None:
    if data:
        raise HTTPException(    
            status_code=status.HTTP,
            detail=error_message,
        )      