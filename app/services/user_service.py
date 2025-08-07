from typing import Dict, List, Tuple

from dataclasses import dataclass
from fastapi import (
    Depends,
    Request, 
    status,
    HTTPException
)
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.connectors.database_connector import get_db
from app.entities.user import User
from app.models.user_models import (
    UserCreationRequest, 
    UserCreationResponse,
    GetUserDetailsResponse,
    UserInfoResponse
)
from app.utils.constants import (
    EMAIL_ALREADY_EXISTS,
    PHONE_NUMBER_ALREADY_EXISTS,
    USER_CREATED_SUCCESSFULLY,
    USER_NOT_FOUND
)
from app.utils.db_queries import (
    get_user_by_email,
    get_user_by_id, 
    get_user_by_phone_number
)
from app.utils.helpers import (
    apply_filter, 
    apply_pagination, 
    apply_sorting, 
    get_all_users
)


@dataclass
class UserService:
    db: Session = Depends(get_db)

    def get_active_user_by_email(self, email: str):
        return (
            self.db.query(User)
            .filter(
                User.email == email,
                User.is_active == True
            ).first()
        )

    def validate_user_details(self, user_details: User):
        if not user_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USER_NOT_FOUND
            )
        
    def _validate_email_not_exists(self, email: str) -> None:
        if get_user_by_email(self.db, email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=EMAIL_ALREADY_EXISTS
            )

    def _validate_phone_not_exists(self, phone_number: str) -> None:
        if get_user_by_phone_number(self.db, phone_number):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=PHONE_NUMBER_ALREADY_EXISTS
            )    
   
    def create_user(
        self, 
        logged_in_user_id: int, 
        request: UserCreationRequest
    ) -> UserCreationResponse:
        self._validate_email_not_exists(request.email)
        self._validate_phone_not_exists(request.phone_number)

        user = User(
            name=request.name,
            email=request.email,
            gender=request.gender,
            password=request.password,
            role=request.role,
            phone_number=request.phone_number,
            created_by=logged_in_user_id,
            updated_by=logged_in_user_id
        )

        self.db.add(user)
        self.db.commit()

        return UserCreationResponse(
            id=user.id,
            message=USER_CREATED_SUCCESSFULLY
        )
    
    def base_get_user_query(self):
        return self.db.query(User)
    
    def get_matched_user_based_on_search(
        self, 
        query, 
        search: str | None, 
    ):
        if search:
            search_pattern = f"%{search.strip()}%"

            query = query.filter(
                or_(
                    User.name.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                    User.phone_number.ilike(search_pattern)
                )
            )    

        return query 
    
    def get_all_user_data(
        self,
        search: str | None,
        filter_by: str | None,
        filter_values: str | None,
        sort_by: str,
        order_by: str,
        page: int | None,
        page_size: int | None
    ) -> Tuple[List[User], int]:
        query = self.base_get_user_query()
        
        query = self.get_matched_user_based_on_search(query, search)
        
        query = apply_filter(
            query=query, 
            main_table=User, 
            filter_by=filter_by, 
            filter_values=filter_values
        )

        query = apply_sorting(
            query=query, 
            table=User, 
            custom_field_sorting=None, 
            sort_by=sort_by, 
            order_by=order_by
        ) 
    
        total_count = query.count()

        if page and page_size:
            query = apply_pagination(query, page, page_size)

        return total_count, query.all()
    
    def get_user_response(
        self, 
        user: User, 
        users: Dict[int, str]
    ) -> GetUserDetailsResponse:

        return GetUserDetailsResponse(
            id=user.id,
            name=user.name, 
            email=user.email,
            gender=user.gender, 
            phone_number=user.phone_number,
            role=user.role,
            created_at=user.created_at,
            created_by=users.get(user.created_by),
            updated_at=user.updated_at,
            updated_by=users.get(user.updated_by),
            is_active=user.is_active
        )
    
    def get_user_responses(
        self,
        search: str | None,
        filter_by: str | None,
        filter_values: str | None,
        sort_by: str,
        order_by: str,
        page: int | None,
        page_size: int | None
    ) -> Tuple[List[GetUserDetailsResponse], int]:
        total_count, users_data = self.get_all_user_data(
            search=search,
            filter_by=filter_by,
            filter_values=filter_values,
            sort_by=sort_by,
            order_by=order_by,
            page=page, 
            page_size=page_size
        )

        users = get_all_users() 

        responses = [
            self.get_user_response(user, users)
            for user in users_data
        ]
        
        return total_count, responses
    
    def get_all_users(
        self,
        search: str | None,
        filter_by: str | None,
        filter_values: str | None,
        sort_by: str,
        order_by: str,
        page: int | None,
        page_size: int | None
    ) -> Tuple[List[GetUserDetailsResponse], int]:
        return self.get_user_responses(
            search=search,
            filter_by=filter_by,
            filter_values=filter_values,
            sort_by=sort_by,
            order_by=order_by,
            page=page, 
            page_size=page_size
        )

    def get_user_by_id(self, user_id: int) -> GetUserDetailsResponse:
        user = get_user_by_id(self.db, user_id)
        self.validate_user_details(user)

        users = get_all_users() 
        return self.get_user_response(user, users)
    
    def get_user_info(self, request_state: Request):
        return UserInfoResponse(
            id=request_state.state.user.id,
            name=request_state.state.user.name,
            email=request_state.state.user.email,
            role=request_state.state.user.role.capitalize()
        )