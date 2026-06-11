from uuid import UUID
from .repository import UserRepository

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