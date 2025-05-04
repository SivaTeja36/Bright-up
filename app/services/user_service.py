from dataclasses import dataclass
from fastapi import (
    Depends, 
    status,
    HTTPException
)
from pydantic import EmailStr
from sqlalchemy.orm import Session
from automapper import mapper
from app.connectors.database_connector import get_db
from app.entities.user import User
from app.models.user_models import (
    UserCreationRequest, 
    UserCreationResponse,
    GetUserDetailsResponse
)
from app.utils.constants import (
    THE_USER_DETAILS_DOES_NOT_EXIST_FOR_THIS_ID
)


@dataclass
class UserService:
    db: Session = Depends(get_db)

    def validate_user_details(self, user_details: User, user_id: int):
        if not user_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=F"{THE_USER_DETAILS_DOES_NOT_EXIST_FOR_THIS_ID} '{user_id}'"
            )


    def create_user(self, request: UserCreationRequest) -> UserCreationResponse:
        user = User()
        user.name = request.name
        user.username = request.username
        user.password = request.password
        user.role = request.role
        user.contact = request.contact
        self.db.add(user)
        self.db.commit()
        return user
    
    def get_all_users(self):
        return [
            mapper.to(GetUserDetailsResponse).map(user_details) 
            for user_details in self.db.query(User).all()
        ]

    def get_user_by_id(self, user_id: int) -> GetUserDetailsResponse:
        user_details = self.db.get(User, user_id)
        self.validate_user_details(user_details, user_id)
        return mapper.to(GetUserDetailsResponse).map(user_details)

    def validate_user(self, username: EmailStr, password: str) -> User | None:
        # this logic should be remvoed once we create some users.
        if self.db.query(User).count() == 0:
            user_request = UserCreationRequest(
                name=username.split("@")[0],
                username=username,
                password=password,
                role="SuperAdmin",
                contact="0987654321",
            )
            return self.create_user(user_request)
        
        user = self.db.query(User).where(User.username == username).first()  # type: ignore

        if user and user.verify_password(password):
            return user
        else:
            return None
