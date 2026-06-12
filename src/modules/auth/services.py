from fastapi import HTTPException, status
from src.modules.auth.models import Token
from src.modules.auth.security import create_access_token, verify_password, password_hasher, create_access_token
from src.modules.users.models import User, UserCreate, UserPublic
from src.modules.users.services import UserService


class AuthService:

    def __init__(self, user_service: UserService) -> None:
        self.user_service: UserService = user_service

    async def login(self, username: str, password: str) -> UserPublic:
        user: User | None = await self.user_service.get_user_by_username(username)

        if not user:                
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        correct_password = verify_password(password, user.hashed_password)

        if not correct_password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        access_token = create_access_token({"sub": user.username})
        

        return Token(access_token=access_token, token_type="bearer")
    

    async def create_user(self, user: UserCreate):
        
        user_instance = user.model_dump()
        
        hashed_pass = password_hasher(user_instance.pop("password"))
        user_instance["hashed_password"] = hashed_pass

        user_created = await self.user_service.create_user(User(**user_instance))

        return user_created