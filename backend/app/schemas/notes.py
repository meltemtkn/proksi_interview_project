from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class Status(str, Enum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Note(BaseModel):
    id: str
    raw_text: str
    summary: str = ""
    status: Status = Status.QUEUED
    user_id: str
    created_at: datetime
    updated_at: datetime

class NoteUpdate(BaseModel):
    id: str
    raw_text: Optional[str] = None
    summary: Optional[str] = None
    status: Optional[Status] = None

class NoteCreate(BaseModel):
    raw_text: str
