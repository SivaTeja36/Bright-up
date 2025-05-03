from typing import Any

from fastapi import (
    HTTPException, 
    status
)


def validate_data_exists(data: Any, error_message: str) -> None:
    if not data:
        raise HTTPException(    
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_message,
        )