from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.models.log import Log
from app.utils.auth import get_current_user, require_admin
from app.response import success

router = APIRouter(prefix="/api/logs", tags=["日志"])


@router.get("")
def list_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    action: str = Query(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Log)

    # Filter by role: admin sees all, others see their own
    if current_user.role.value != "admin":
        q = q.filter(Log.user_id == current_user.id)

    if action:
        q = q.filter(Log.action == action)

    total = q.count()
    items = q.order_by(Log.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return success({
        "items": [{
            "id": log.id,
            "userId": log.user_id,
            "username": log.username,
            "action": log.action,
            "targetType": log.target_type,
            "targetId": log.target_id,
            "detail": log.detail,
            "ip": log.ip or "",
            "result": log.result,
            "createdAt": log.created_at.isoformat() if log.created_at else "",
        } for log in items],
        "total": total,
        "page": page,
        "pageSize": page_size,
    })
