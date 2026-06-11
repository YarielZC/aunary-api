from uuid import UUID
from typing import Sequence
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncScalarResult
from sqlmodel import select
from .models import User

class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def get_all(self) -> Sequence[User]:
        statement = select(User)
        result: AsyncScalarResult[User] = await self.session.exec(statement)
        return result.all()
    
    async def get_by_id(self, user_id: UUID) -> User | None:
        statement = select(User).where(User.id == user_id)
        result: AsyncScalarResult[User] = await self.session.exec(statement)
        return result.one_or_none()
