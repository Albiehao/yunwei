from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.models.schedule import Schedule
from app.models.server import Server
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate
from app.utils.auth import get_current_user
from app.response import success, error

router = APIRouter(prefix="/api/schedules", tags=["定时任务"])


@router.get("")
def list_schedules(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    schedules = db.query(Schedule).filter(Schedule.user_id == current_user.id).all()
    result = []
    for s in schedules:
        server = db.query(Server).filter(Server.id == s.server_id).first()
        result.append({
            "id": s.id,
            "name": s.name,
            "server_id": s.server_id,
            "server_name": server.name if server else None,
            "action": s.action.value if hasattr(s.action, 'value') else s.action,
            "cron_expression": s.cron_expression,
            "timezone": s.timezone,
            "enabled": s.enabled,
            "last_run_at": s.last_run_at,
            "next_run_at": s.next_run_at,
            "created_at": s.created_at,
            "updated_at": s.updated_at,
        })
    return success(result)


@router.post("")
def create_schedule(data: ScheduleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    server = db.query(Server).filter(Server.id == data.server_id).first()
    if not server:
        return error("服务器不存在", 404)
    schedule = Schedule(
        name=data.name,
        server_id=data.server_id,
        action=data.action,
        cron_expression=data.cron_expression,
        timezone=data.timezone,
        enabled=data.enabled,
        user_id=current_user.id,
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return success({
        "id": schedule.id,
        "name": schedule.name,
        "server_id": schedule.server_id,
        "server_name": server.name,
        "action": schedule.action.value if hasattr(schedule.action, 'value') else schedule.action,
        "cron_expression": schedule.cron_expression,
        "timezone": schedule.timezone,
        "enabled": schedule.enabled,
        "created_at": schedule.created_at,
        "updated_at": schedule.updated_at,
    })


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
    return success({
        "id": schedule.id,
        "name": schedule.name,
        "server_id": schedule.server_id,
        "server_name": server.name if server else None,
        "action": schedule.action.value if hasattr(schedule.action, 'value') else schedule.action,
        "cron_expression": schedule.cron_expression,
        "timezone": schedule.timezone,
        "enabled": schedule.enabled,
        "last_run_at": schedule.last_run_at,
        "next_run_at": schedule.next_run_at,
        "created_at": schedule.created_at,
        "updated_at": schedule.updated_at,
    })


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
