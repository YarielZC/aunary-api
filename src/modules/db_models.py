from sqlmodel import SQLModel
from .users.models import User

metadata = SQLModel.metadata
