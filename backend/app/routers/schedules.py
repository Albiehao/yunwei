from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.models.schedule import Schedule
from app.models.server import Server
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate
from app.utils.auth import get_current_user
from app.response import success, error


def _fmt(s: Schedule, server_name: str = "") -> dict:
    return {
        "id": str(s.id),
        "name": s.name,
        "serverId": s.server_id,
        "serverName": server_name or s.server_id,
        "action": s.action.value if hasattr(s.action, "value") else s.action,
        "cronExpression": s.cron_expression,
        "timezone": s.timezone,
        "enabled": s.enabled,
        "lastRunAt": s.last_run_at.isoformat() if s.last_run_at else None,
        "nextRunAt": s.next_run_at.isoformat() if s.next_run_at else None,
        "createdAt": s.created_at.isoformat() if s.created_at else "",
        "updatedAt": s.updated_at.isoformat() if s.updated_at else "",
    }


router = APIRouter(prefix="/api/schedules", tags=["定时任务"])


@router.get("")
def list_schedules(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    schedules = db.query(Schedule).filter(Schedule.user_id == current_user.id).all()
    result = []
    for s in schedules:
        server = db.query(Server).filter(Server.id == s.server_id).first()
        result.append(_fmt(s, server.name if server else ""))
    return success(result)


@router.post("")
def create_schedule(data: ScheduleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sid = data.serverId
    server = db.query(Server).filter(Server.id == sid).first()
    if not server:
        return error("服务器不存在", 404)
    schedule = Schedule(
        name=data.name,
        server_id=sid,
        action=data.action,
        cron_expression=data.cronExpression,
        timezone=data.timezone,
        enabled=data.enabled,
        user_id=current_user.id,
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return success(_fmt(schedule, server.name))


@router.put("/{schedule_id}")
def update_schedule(schedule_id: int, data: ScheduleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id, Schedule.user_id == current_user.id).first()
    if not schedule:
        return error("定时任务不存在", 404)
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(schedule, key, val)
    db.commit()
    db.refresh(schedule)
    server = db.query(Server).filter(Server.id == schedule.server_id).first()
    return success(_fmt(schedule, server.name if server else ""))


@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id, Schedule.user_id == current_user.id).first()
    if not schedule:
        return error("定时任务不存在", 404)
    db.delete(schedule)
    db.commit()
    return success(None, "删除成功")


@router.patch("/{schedule_id}/toggle")
def toggle_schedule(schedule_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id, Schedule.user_id == current_user.id).first()
    if not schedule:
        return error("定时任务不存在", 404)
    schedule.enabled = not schedule.enabled
    db.commit()
    return success({"enabled": schedule.enabled})
