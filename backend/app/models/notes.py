from typing import TYPE_CHECKING
from sqlalchemy import Column, String, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from .base import BaseModel
from enum import Enum

if TYPE_CHECKING:
    from .users import User

class Status(str, Enum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed" 

class Note(BaseModel):
    __tablename__ = "notes"

    status = Column(SQLAlchemyEnum(Status, name="status"), nullable=False)
    raw_text = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="notes")