from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from src.modules.auth.dependencies import get_current_public_user
from src.modules.auth.services import AuthService
from src.modules.users.models import UserCreate, UserPublic
from src.modules.auth.dependencies import get_auth_service
from src.modules.auth.models import Token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/me", response_model=UserPublic, status_code=status.HTTP_200_OK)
async def get_my_info(current_user: Annotated[UserPublic, Depends(get_current_public_user)]):
    return current_user

@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login(login_form: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: AuthService = Depends(get_auth_service)):

    token: Token = await auth_service.login(username=login_form.username, password=login_form.password)
    
    return token

@router.post("/sign_up", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def sign_up(user_form: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    user: UserPublic = await auth_service.create_user(user_form)
    return user