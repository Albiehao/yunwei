import json
import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.models.task import Task, TaskStatus, TaskAction
from app.utils.auth import get_current_user
from app.aliyun_client import delete_ecs_instance
from app.response import success, error

router = APIRouter(prefix="/api/tasks", tags=["任务"])


@router.get("")
def list_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    q = db.query(Task)
    if current_user.role.value != "admin":
        q = q.filter(Task.user_id == current_user.id)
    tasks = q.order_by(Task.created_at.desc()).limit(100).all()
    return success([{
        "id": t.id,
        "action": t.action.value,
        "serverId": t.server_id or "",
        "serverName": t.server_name or "",
        "params": json.loads(t.params) if t.params else {},
        "status": t.status.value,
        "message": t.message or "",
        "createdAt": t.created_at.isoformat() if t.created_at else "",
        "doneAt": t.done_at.isoformat() if t.done_at else "",
        "userId": t.user_id,
    } for t in tasks])


@router.post("")
def create_task(body: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    action = body.get("action", "")
    server_id = body.get("serverId", "")
    server_name = body.get("serverName", "")

    if action not in ("release", "purchase"):
        return error("不支持的任务类型", 400)

    params = {}
    if action == "purchase":
        params = {
            "instanceType": body.get("instanceType", ""),
            "region": body.get("region", ""),
            "name": body.get("name", ""),
            "quantity": body.get("quantity", 1),
        }

    task = Task(
        action=TaskAction.PURCHASE if action == "purchase" else TaskAction.RELEASE,
        server_id=server_id,
        server_name=server_name,
        params=json.dumps(params),
        status=TaskStatus.PENDING,
        user_id=current_user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return success({
        "id": task.id,
        "action": task.action.value,
        "serverId": task.server_id or "",
        "serverName": task.server_name or "",
        "params": params,
        "status": task.status.value,
        "createdAt": task.created_at.isoformat(),
    })


@router.post("/{task_id}/execute")
def execute_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return error("任务不存在", 404)
    if task.status != TaskStatus.PENDING:
        return error("任务已执行", 400)

    if task.action == TaskAction.RELEASE:
        ok = delete_ecs_instance(task.server_id)
        if ok:
            task.status = TaskStatus.DONE
            task.message = "释放成功"
        else:
            task.status = TaskStatus.FAILED
            task.message = "释放失败"
    elif task.action == TaskAction.PURCHASE:
        params = json.loads(task.params) if task.params else {}
        task.status = TaskStatus.DONE
        task.message = f"购买成功: {params.get('instanceType', '')} x{params.get('quantity', 1)}（模拟）"
    else:
        return error("不支持的任务类型", 400)

    task.done_at = datetime.datetime.utcnow()
    db.commit()
    return success({"id": task.id, "status": task.status.value, "message": task.message})


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        return error("任务不存在", 404)
    db.delete(task)
    db.commit()
    return success(None, "已删除")
