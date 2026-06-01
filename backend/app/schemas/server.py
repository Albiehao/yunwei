from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.server import ServerStatus, ChargeType


class ServerOut(BaseModel):
    id: int
    name: str
    instance_type: str
    status: ServerStatus
    region: str
    ip_address: Optional[str] = None
    cpu: int
    memory: int
    disk: int
    bandwidth: int
    charge_type: ChargeType
    created_at: datetime
    expired_at: Optional[datetime] = None
    tags: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)


class ServerActionResponse(BaseModel):
    success: bool
    message: str
