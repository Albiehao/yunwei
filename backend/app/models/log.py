import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database import Base


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    username = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False)  # start, stop, release, exec_ssh, create_schedule, etc.
    target_type = Column(String(50), nullable=True)  # server, schedule, user, system
    target_id = Column(String(100), nullable=True)
    detail = Column(Text, nullable=True)
    ip = Column(String(50), nullable=True)
    result = Column(String(20), default="success")  # success, failed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
