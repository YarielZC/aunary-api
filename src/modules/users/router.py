from fastapi import APIRouter, Depends, status

from src.modules.users.models import User, UserCreate, UserPublic
from .services import UserService
from .dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserPublic])
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    return await user_service.get_all()

@router.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def create_user(user_in: UserCreate, user_service: UserService = Depends(get_user_service)):
    return await user_service.create_user(user_in)

