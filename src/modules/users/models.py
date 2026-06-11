import uuid

from typing import Optional
from sqlmodel import SQLModel, Field

from src.core.mixins import TimeStampModel

class UserBase(SQLModel):
    email: str = Field(max_length=255, unique=True, nullable=False, index=True)
    full_name: str = Field(max_length=100, nullable=False)
    bio: Optional[str] = None
    avatar_url: str | None = Field(max_length=511, nullable=True, default=None)
    portfolio_url: str | None = Field(max_length=511, nullable=True, default=None)
    
class User(UserBase, TimeStampModel, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )
    hashed_password: str = Field(max_length=255, nullable=True)
    is_active: bool = Field(default=True)

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase, TimeStampModel):
    id: uuid.UUID
    is_active: bool
