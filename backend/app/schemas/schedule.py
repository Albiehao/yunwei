from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.schedule import ScheduleAction


class ScheduleOut(BaseModel):
    id: int
    name: str
    server_id: int
    server_name: Optional[str] = None
    action: ScheduleAction
    cron_expression: str
    timezone: str
    enabled: bool
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ScheduleCreate(BaseModel):
    name: str
    server_id: int
    action: ScheduleAction
    cron_expression: str
    timezone: str = "Asia/Shanghai"
    enabled: bool = True


class ScheduleUpdate(BaseModel):
    name: Optional[str] = None
    server_id: Optional[int] = None
    action: Optional[ScheduleAction] = None
    cron_expression: Optional[str] = None
    timezone: Optional[str] = None
    enabled: Optional[bool] = None
