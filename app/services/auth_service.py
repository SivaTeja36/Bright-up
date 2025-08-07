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
from app.utils.constants import (
    INCORRECT_PASSWORD, 
    USER_NOT_FOUND
)


@dataclass
class AuthService:
    user_service: UserService = Depends(UserService)
    
    def create_claims(self, user: User):
        claims = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "phone_number": user.phone_number,
                "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            }
        return claims
    
    def generate_token_response(self, claims: dict) -> LoginResponse:
        """
            Generate JWT token and return the login response.
        """
        try:
            token = jwt.encode(
                claims=claims, 
                key=SECRET_KEY, 
                algorithm=ALGORITHM
            )
            return LoginResponse(
                token=token,
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


    def login(self, request: LoginRequest) -> LoginResponse:
        """
            Authenticate a user and generate a JWT token upon successful login.
        """
        user = self.user_service.get_active_user_by_email(request.email)
        
        if user:
            if user.verify_password(request.password):
                claims = self.create_claims(user)
                
                return self.generate_token_response(
                    claims=claims
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=INCORRECT_PASSWORD
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=USER_NOT_FOUND
            )