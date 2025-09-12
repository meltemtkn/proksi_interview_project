from typing import TYPE_CHECKING
from sqlalchemy import Column, String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from .base import BaseModel
from enum import Enum

if TYPE_CHECKING:
    from .notes import Note

class Role(str, Enum):
    ADMIN = "admin"
    AGENT = "agent"
    WORKER = "worker"

class User(BaseModel):
    __tablename__ = "users"

    role = Column(SQLAlchemyEnum(Role, name="role"), nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)

    notes = relationship("Note", back_populates="user")