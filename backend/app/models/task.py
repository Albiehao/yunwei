import datetime
import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum
from app.database import Base


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    DONE = "done"
    FAILED = "failed"


class TaskAction(str, enum.Enum):
    RELEASE = "release"
    PURCHASE = "purchase"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(SAEnum(TaskAction), nullable=False)
    server_id = Column(String(50), nullable=True)
    server_name = Column(String(100), default="")
    params = Column(String(500), nullable=True)  # JSON for purchase details
    status = Column(SAEnum(TaskStatus), default=TaskStatus.PENDING)
    message = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    done_at = Column(DateTime, nullable=True)
    user_id = Column(Integer, nullable=False, index=True)
