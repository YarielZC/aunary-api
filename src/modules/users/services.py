from uuid import UUID

from src.modules.users.models import UserPublic, User
from .repository import UserRepository

from fastapi import status, HTTPException
class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_all(self):
        return await self.user_repository.get_all()
    
    async def get_by_id(self, user_id: UUID):
        user = await self.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")
        
        return user
    
    async def get_user_by_username(self, username: str) -> User | None:
        return await self.user_repository.get_user_by_username(username)
    
    async def create_user(self, user: User) -> UserPublic:

        try:
            return await self.user_repository.create_user(user)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))