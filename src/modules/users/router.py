from fastapi import APIRouter, Depends
from .services import UserService
from .dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[dict])
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    return await user_service.get_all()

