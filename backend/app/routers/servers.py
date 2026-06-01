from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User
from app.models.server import Server, ServerStatus
from app.schemas.server import ServerOut, ServerActionResponse
from app.utils.auth import get_current_user
from app.aliyun_client import list_ecs_instances, start_ecs_instance, stop_ecs_instance
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/servers", tags=["服务器"])


@router.get("", response_model=List[ServerOut])
def list_servers(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """获取服务器列表，优先从阿里云拉取实时数据"""
    aliyun_instances = list_ecs_instances()
    if aliyun_instances:
        # 同步到本地数据库
        for inst in aliyun_instances:
            existing = db.query(Server).filter(Server.id == inst["id"]).first()
            if existing:
                for k, v in inst.items():
                    if k in ("id", "name", "instance_type", "status", "region",
                             "ip_address", "cpu", "memory", "disk", "bandwidth",
                             "charge_type"):
                        setattr(existing, k, v)
            else:
                server = Server(
                    id=inst["id"],
                    name=inst["name"],
                    instance_type=inst["instance_type"],
                    status=inst["status"],
                    region=inst["region"],
                    ip_address=inst["ip_address"],
                    cpu=inst["cpu"],
                    memory=inst["memory"],
                    disk=inst["disk"],
                    bandwidth=inst["bandwidth"],
                    charge_type=inst["charge_type"],
                    user_id=current_user.id,
                )
                db.add(server)
        db.commit()
        return aliyun_instances

    # 无阿里云配置时读本地 DB
    servers = db.query(Server).filter(Server.user_id == current_user.id).all()
    return servers


@router.post("/{server_id}/start", response_model=ServerActionResponse)
def start_server(server_id: str, current_user: User = Depends(get_current_user)):
    """启动服务器"""
    ok = start_ecs_instance(server_id)
    if not ok:
        raise HTTPException(status_code=500, detail="启动失败，请检查阿里云配置")
    return ServerActionResponse(success=True, message="启动指令已发送")


@router.post("/{server_id}/stop", response_model=ServerActionResponse)
def stop_server(server_id: str, current_user: User = Depends(get_current_user)):
    """停止服务器"""
    ok = stop_ecs_instance(server_id)
    if not ok:
        raise HTTPException(status_code=500, detail="停止失败，请检查阿里云配置")
    return ServerActionResponse(success=True, message="停止指令已发送")
