from pydantic import BaseModel, Field
from typing import Optional
from app.models.schedule import ScheduleAction


class ScheduleCreate(BaseModel):
    name: str
    serverId: str = Field(alias="server_id")
    action: ScheduleAction
    cronExpression: str = Field(alias="cron_expression")
    timezone: str = "Asia/Shanghai"
    enabled: bool = True

    model_config = {"populate_by_name": True}


class ScheduleUpdate(BaseModel):
    name: Optional[str] = None
    serverId: Optional[str] = Field(None, alias="server_id")
    action: Optional[ScheduleAction] = None
    cronExpression: Optional[str] = Field(None, alias="cron_expression")
    timezone: Optional[str] = None
    enabled: Optional[bool] = None

    model_config = {"populate_by_name": True}
