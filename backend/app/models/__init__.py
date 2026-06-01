import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as SAEnum, JSON
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    DEVELOPER = "developer"
    AUDITOR = "auditor"


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    DISABLED = "disabled"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole), default=UserRole.DEVELOPER, nullable=False)
    status = Column(SAEnum(UserStatus), default=UserStatus.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
