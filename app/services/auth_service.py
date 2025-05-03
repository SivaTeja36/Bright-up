from datetime import (
    datetime, 
    timedelta
)
from dataclasses import dataclass
from jose import jwt
from fastapi import (
    Depends,
    status,
    HTTPException,
)
from app.entities.user import User
from app.models.auth_models import (
    LoginRequest, 
    LoginResponse
)
from .user_service import UserService
from app.utils.auth_dependencies import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)
from app.utils.constants import USER_NOT_FOUND

@dataclass
class AuthService:
    user_serivce: UserService = Depends(UserService)
    
    def create_claims(self, user: User):
        claims = {
                "sub": str(user.username),
                "role": user.role,
                "name": user.name,
                "contact": user.contact,
                "user_id": user.id,
                "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            }
        return claims


    def login(self, request: LoginRequest):
        user = self.user_serivce.validate_user(request.userName, request.password)

        if user and user.verify_password(request.password):
            claims = self.create_claims(user)
            try:
                token = jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)
                return LoginResponse(
                    access_token=token,
                    name=user.name,
                    role=user.role,
                    contact=user.contact,
                    id=user.id,
                )
            except Exception as e:
                print(e)
                raise e
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=USER_NOT_FOUND
        )
