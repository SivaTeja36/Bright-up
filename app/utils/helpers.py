from typing import Any, Dict

from fastapi import (
    HTTPException, 
    status
)
from sqlalchemy.orm import Session

from app.connectors.database_connector import get_database, get_db
from app.utils.constants import COLUMN_NOT_FOUND
from app.utils.db_queries import get_users
from app.utils.enums import OrderByTypes


def get_all_users_dict(db: Session) -> dict:
    """
    Get all users from the database and return them as a dictionary.
    """
    users = get_users(db)
    return {user.id: user.name for user in users}

def get_all_users_dict(db: Session) -> Dict[int, str]:
    return {
        user.id: user.name
        for user in get_users(db)
    }

def get_all_users() -> Dict[int, str]:
    with get_database() as db:
        users = get_all_users_dict(db)

    return users   

def apply_filter(
    query, 
    main_table: Any, 
    filter_by: str | None, 
    filter_values: str | None, 
    related_table: Any = None, 
    related_table_column: str = None
):
    """
        Apply dynamic filtering to the SQLAlchemy query based on the provided filter criteria.
    """

    if not filter_by or not filter_values:
        return query  

    columns = list(map(str.strip, filter_by.split(",")))
    values = list(map(str.strip, filter_values.split(",")))

    if len(columns) != len(values):
        raise ValueError("Mismatch between number of filter columns and values.")

    for column, value in zip(columns, values):
        value = True if value.lower() == "true" else False if value.lower() == "false" else value.strip()

        target_table = related_table if column.strip() == related_table_column else main_table

        if not hasattr(target_table, column.strip()):
            raise AttributeError(f"Column '{column}' not found in '{target_table.__name__}'.")

        query = query.filter(getattr(target_table, column.strip()) == value)

    return query

def apply_sorting(query, table: Any, custom_field_sorting: Any, sort_by: str, order_by: str):
    if custom_field_sorting is None:
        try:
            sort_column = getattr(table, sort_by.strip().lower())
        except AttributeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=COLUMN_NOT_FOUND
            )  
    else:
        sort_column = custom_field_sorting    

    if order_by == OrderByTypes.DESC:
        return query.order_by(sort_column.desc())
    
    return query.order_by(sort_column.asc())  

#┌────────────────────────────── PAGINATION SERVICE ──────────────────────────────────────────┐

def get_offset_value(page: int, page_size: int) -> int:
    return (page - 1) * page_size


def apply_pagination(query, page: int, page_size: int):
    """
        Apply pagination to the query.
    """
    offset = get_offset_value(page, page_size)
    return query.limit(page_size).offset(offset)
