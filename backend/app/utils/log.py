from sqlalchemy.orm import Session
from app.models.log import Log


def add_log(
    db: Session,
    user_id: int,
    username: str,
    action: str,
    target_type: str = None,
    target_id: str = None,
    detail: str = None,
    ip: str = None,
    result: str = "success",
):
    log = Log(
        user_id=user_id,
        username=username,
        action=action,
        target_type=target_type,
        target_id=target_id,
        detail=detail,
        ip=ip,
        result=result,
    )
    db.add(log)
    db.commit()
