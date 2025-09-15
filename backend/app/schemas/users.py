from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum
from datetime import timezone

class Role(str, Enum):
    ADMIN = "admin"
    AGENT = "agent"
    WORKER = "worker"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Role = Role.AGENT  # Default to AGENT role

class UserResponse(BaseModel):
    id: str
    email: str
    role: Role
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class User(BaseModel):
    id: str
    email: str
    password: str
    role: Role
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserUpdate(BaseModel):
    id: str
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[Role] = None