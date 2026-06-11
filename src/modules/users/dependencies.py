from sqlalchemy.ext.asyncio import AsyncSession
from .repository import UserRepository
from .services import UserService
from fastapi import Depends
from src.core.database import get_session

def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)