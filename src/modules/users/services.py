from uuid import UUID

from src.modules.users.models import UserCreate, UserPublic, User
from .repository import UserRepository

from fastapi import status

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
    
    async def create_user(self, user: UserCreate) -> UserPublic:

        try:
            hashed_pw_mock = user.password + "_hashed"

            user_data = user.model_dump(exclude={"password"})

            user_data["hashed_password"] = hashed_pw_mock

            
            return await self.user_repository.create_user(User(**user_data))
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))