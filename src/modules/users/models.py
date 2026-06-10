import uuid

from typing import Optional
from sqlmodel import SQLModel, Field

from src.core.mixins import TimeStampModel


class User(TimeStampModel, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )
    email: str = Field(max_length=255, unique=True, nullable=False, index=True)
    hashed_password: str = Field(max_length=255, nullable=True)
    full_name: str = Field(max_length=100, nullable=False)
    bio: Optional[str] = None
    avatar_url: str = Field(max_length=511, nullable=True)
    portfolio_url: str = Field(max_length=511, nullable=True)
