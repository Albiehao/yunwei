import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum, JSON
from app.database import Base
import enum


class ServerStatus(str, enum.Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    STARTING = "starting"
    STOPPING = "stopping"
    PENDING = "pending"
    ERROR = "error"


class ChargeType(str, enum.Enum):
    POSTPAID = "PostPaid"
    PREPAID = "PrePaid"


class Server(Base):
    __tablename__ = "servers"

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False, index=True)
    instance_type = Column(String(50), nullable=False)
    status = Column(SAEnum(ServerStatus), default=ServerStatus.PENDING, nullable=False)
    region = Column(String(50), nullable=False)
    ip_address = Column(String(15), nullable=True)
    cpu = Column(Integer, default=2)
    memory = Column(Integer, default=4)
    disk = Column(Integer, default=20)
    bandwidth = Column(Integer, default=50)
    charge_type = Column(SAEnum(ChargeType), default=ChargeType.POSTPAID)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expired_at = Column(DateTime, nullable=True)
    tags = Column(JSON, nullable=True)
    remark = Column(String(200), nullable=True)
    user_id = Column(Integer, nullable=False, index=True)
