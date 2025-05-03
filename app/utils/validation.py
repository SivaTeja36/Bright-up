from typing import Any

from fastapi import (
    HTTPException
)


def validate_data_exists(data: Any, error_message: str, status_code: int = 404) -> None:
    if not data:
        raise HTTPException(    
            status_code=status_code,
            detail=error_message,
        )  