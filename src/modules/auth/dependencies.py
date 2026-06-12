from typing import Annotated
from fastapi import Depends, HTTPException

from src.modules.auth.services import AuthService
from src.modules.users.dependencies import get_user_service
from src.modules.users.services import UserService
from src.modules.users.models import User, UserPublic
from .security import decode_token
from fastapi.security.oauth2 import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_token_payload(token: str) -> dict:
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException("Invalid credentials")
    
    return payload

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_service: UserService = Depends(get_user_service)) -> User:
    
    payload = get_token_payload(token)

    username = payload.get("sub")

    if not username:
        raise HTTPException("Invalid credentials")
    
    user = await user_service.get_user_by_username(username)
    
    if not user:
        raise HTTPException("Invalid credentials")
    
    return user

async def get_current_public_user(current_user: User = Depends(get_current_user)) -> UserPublic:
    return UserPublic.model_validate(current_user)

def get_auth_service(user_service: UserService = Depends(get_user_service)) -> AuthService:
    return AuthService(user_service=user_service)


