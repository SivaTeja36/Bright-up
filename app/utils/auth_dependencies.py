import os

from dotenv import load_dotenv
from jose import jwt
from fastapi import (
    Request, 
    HTTPException, 
    status
)

from app.models.user_models import CurrentContextUser
from app.utils.constants import (
    AUTHORIZATION, 
    INVALID_TOKEN
)

load_dotenv()

SECRET_KEY: str = os.getenv("JWT_SECRET")  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300  


def get_token_payload(token: str) -> dict:
    """
    Decodes a JWT token and returns its payload.
    """
    token = token.replace("Bearer ", "")
   
    try:
        payload = jwt.decode(
            token=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_sub": True}
        )
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )

def __verify_jwt(token: str):
    payload = get_token_payload(token)
    user_email = payload.get("email")
    
    if user_email:
        cur_user = CurrentContextUser()
        cur_user.id = payload.get("id")
        cur_user.name = payload.get("name")
        cur_user.email = user_email
        cur_user.role = payload.get("role")
        
        return cur_user

async def verify_auth_token(request: Request):
    if (
        "login" not in request.url.path
        and "refresh" not in request.url.path
    ):
        auth: str = request.headers.get(AUTHORIZATION) or ""
        
        try:
            request.state.user = __verify_jwt(token=auth)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INVALID_TOKEN 
            )
