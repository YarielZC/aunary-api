from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, future=True, pool_size=20, max_overflow=10)


async def get_session() -> AsyncGenerator[AsyncSession, None]:

    async with AsyncSession(bind=engine, expire_on_commit=False) as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
