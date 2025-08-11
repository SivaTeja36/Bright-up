from datetime import datetime
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
from app.entities.user_education import UserEducation
from app.models.user_models import (
    UpdateUserPassword,
    UpdateUserRequest,
    UserCreationRequest,
    UserEducationResponse, 
    UserResponse,
    GetUserDetailsResponse,
    UserInfoResponse
)
from app.utils.constants import (
    EMAIL_ALREADY_EXISTS,
    PHONE_NUMBER_ALREADY_EXISTS,
    USER_CREATED_SUCCESSFULLY,
    USER_NOT_FOUND,
    USER_PASSWORD_UPDATED_SUCCESSFULLY,
    USER_UPDATED_SUCCESSFULLY
)
from app.utils.db_queries import (
    get_user_by_email,
    get_user_by_id, 
    get_user_by_phone_number,
    get_user_education_by_id
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

    def add_user(self, request: UserCreationRequest, logged_in_user_id: int) -> User:
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

        return user
        
    def add_user_education(
        self, 
        user_id: int, 
        request: UserCreationRequest, 
        logged_in_user_id: int
    ) -> None:
        user_education = UserEducation(
            user_id=user_id,
            degree=request.education.degree,
            specialization=request.education.specialization,
            start_year=request.education.start_year,
            end_year=request.education.end_year,
            current_year_of_study=request.education.current_year_of_study,
            status=request.education.status,
            city=request.education.city,
            state=request.education.state,
            created_by=logged_in_user_id,
            updated_by=logged_in_user_id
        ) 

        self.db.add(user_education)
        self.db.commit()
   
    def create_user(
        self, 
        logged_in_user_id: int, 
        request: UserCreationRequest
    ) -> UserResponse:
        self._validate_email_not_exists(request.email)
        self._validate_phone_not_exists(request.phone_number)

        user = self.add_user(request, logged_in_user_id)
        self.add_user_education(user.id, request, logged_in_user_id)

        return UserResponse(
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
    
    def get_user_education_response(
        self, 
        user_education: UserEducation,
        users: Dict[int, str]
    ) -> UserEducationResponse:
        return UserEducationResponse(
            id=user_education.id, 
            degree=user_education.degree, 
            specialization=user_education.specialization, 
            start_year=user_education.start_year, 
            end_year=user_education.end_year, 
            current_year_of_study=user_education.current_year_of_study,
            status=user_education.status, 
            city=user_education.city, 
            state=user_education.state, 
            created_at=user_education.created_at,
            created_by=users.get(user_education.created_by),
            updated_at=user_education.updated_at,
            updated_by=users.get(user_education.updated_by),
        )
    
    def get_user_response(
        self, 
        user: User, 
        users: Dict[int, str]
    ) -> GetUserDetailsResponse:
        user_education_details = get_user_education_by_id(self.db, user.id)
        user_education = self.get_user_education_response(user_education_details, users)

        return GetUserDetailsResponse(
            id=user.id,
            name=user.name, 
            email=user.email,
            gender=user.gender, 
            phone_number=user.phone_number,
            role=user.role,
            education=user_education,
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
    
    def update_user(
        self, 
        user: User, 
        request: UpdateUserRequest, 
        logged_in_user_id: int
    ) -> None:
        user.name = request.name
        user.gender = request.gender
        user.role = request.role
        user.phone_number = request.phone_number
        user.updated_at = datetime.now()
        user.updated_by = logged_in_user_id
    
    def update_user_education(
        self, 
        user_education: UserEducation, 
        request: UpdateUserRequest, 
        logged_in_user_id: int
    ) -> None:
        user_education.degree = request.education.degree
        user_education.specialization = request.education.specialization
        user_education.start_year = request.education.start_year
        user_education.end_year = request.education.end_year
        user_education.current_year_of_study = request.education.current_year_of_study
        user_education.status = request.education.status
        user_education.city = request.education.city
        user_education.state = request.education.state
        user_education.updated_at = datetime.now()
        user_education.updated_by = logged_in_user_id
    
    def update_user_by_id(
        self, 
        logged_in_user_id: int, 
        user_id: int, 
        request: UpdateUserRequest
    ) -> UserResponse:
        user = get_user_by_id(self.db, user_id)
        self.validate_user_details(user)
        user_education = get_user_education_by_id(self.db, user_id)
        
        if request.is_active is not None:
            user.is_active = request.is_active
            user.updated_at = datetime.now()
            user.updated_by = logged_in_user_id
        else:
            self.update_user(user, request, logged_in_user_id)
            self.update_user_education(user_education, request, logged_in_user_id)

        self.db.commit()
        
        return UserResponse(
            id=user_id,
            message=USER_UPDATED_SUCCESSFULLY
        )
    
    def update_user_password(
        self, 
        logged_in_user_id: int, 
        request: UpdateUserPassword
    ) -> UserResponse:
        user = get_user_by_id(self.db, logged_in_user_id)
        self.validate_user_details(user)

        user.password = request.password
        user.updated_at = datetime.now()
        user.updated_by = logged_in_user_id

        self.db.commit()

        return UserResponse(
            id=logged_in_user_id,
            message=USER_PASSWORD_UPDATED_SUCCESSFULLY
        )

    def get_user_info(self, request_state: Request):
        return UserInfoResponse(
            id=request_state.state.user.id,
            name=request_state.state.user.name,
            email=request_state.state.user.email,
            role=request_state.state.user.role.capitalize()
        )