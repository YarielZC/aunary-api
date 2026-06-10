from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, text
from datetime import datetime


class TimeStampModel(SQLModel):
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("CURRENT_TIMESTAMP"),
            nullable=False,
        )
    )

    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("CURRENT_TIMESTAMP"),
            onupdate=text("CURRENT_TIMESTAMP"),
            nullable=False,
        )
    )
