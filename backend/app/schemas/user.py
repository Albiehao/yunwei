from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models import UserRole, UserStatus


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    phone: Optional[str] = None
    role: UserRole
    status: UserStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    phone: Optional[str] = None
    role: UserRole = UserRole.DEVELOPER


class UserUpdate(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
