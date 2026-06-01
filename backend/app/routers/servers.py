from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User
from app.models.server import Server, ServerStatus
from app.schemas.server import ServerOut
from app.utils.auth import get_current_user
from app.aliyun_client import list_ecs_instances, start_ecs_instance, stop_ecs_instance
from app.response import success, error
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/servers", tags=["服务器"])


@router.get("")
def list_servers(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """获取服务器列表，优先从阿里云拉取实时数据"""
    aliyun_instances = list_ecs_instances()
    if aliyun_instances:
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
                    user_id=int(current_user.id) if str(current_user.id).isdigit() else 1,
                )
                db.add(server)
        db.commit()
        return success(aliyun_instances)

    servers = db.query(Server).filter(Server.user_id == current_user.id).all()
    return success(servers)


@router.post("/{server_id}/start")
def start_server(server_id: str, current_user: User = Depends(get_current_user)):
    ok = start_ecs_instance(server_id)
    if not ok:
        return error("启动失败，请检查阿里云配置", 500)
    return success({"success": True}, "启动指令已发送")


@router.post("/{server_id}/stop")
def stop_server(server_id: str, current_user: User = Depends(get_current_user)):
    ok = stop_ecs_instance(server_id)
    if not ok:
        return error("停止失败，请检查阿里云配置", 500)
    return success({"success": True}, "停止指令已发送")
