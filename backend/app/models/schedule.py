import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as SAEnum
from app.database import Base
import enum


class ScheduleAction(str, enum.Enum):
    START = "start"
    STOP = "stop"


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    server_id = Column(String(50), nullable=False, index=True)
    action = Column(SAEnum(ScheduleAction), nullable=False)
    cron_expression = Column(String(50), nullable=False)
    timezone = Column(String(50), default="Asia/Shanghai")
    enabled = Column(Boolean, default=True)
    last_run_at = Column(DateTime, nullable=True)
    next_run_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    user_id = Column(Integer, nullable=False, index=True)
