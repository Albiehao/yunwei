from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.models.server import Server
from app.utils.auth import get_current_user
from app.utils.log import add_log
import json
import time
from app.aliyun_client import list_ecs_instances, start_ecs_instance, stop_ecs_instance, delete_ecs_instance
from aliyunsdkcms.request.v20190101 import DescribeMetricListRequest, DescribeMetricLastRequest
from app.response import success, error
from app.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/servers", tags=["服务器"])


@router.get("")
def list_servers(
    region: str = Query(default="", description="阿里云地域, 默认从.env读取"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取服务器列表，从阿里云拉取实时数据"""
    r = region if region else settings.ALIYUN_REGION
    aliyun_instances = list_ecs_instances(region_override=r)
    if aliyun_instances:
        for inst in aliyun_instances:
            spec = inst.get("spec", {})
            remark = ""
            existing = db.query(Server).filter(Server.id == inst["id"]).first()
            if existing:
                existing.status = inst.get("status", existing.status)
                existing.ip_address = inst.get("ipAddress", existing.ip_address)
                existing.charge_type = inst.get("chargeType", existing.charge_type)
                existing.cpu = spec.get("cpu", existing.cpu)
                mem = spec.get("memory", 0)
                existing.memory = mem // 1024 if mem > 1024 else mem
                remark = existing.remark or ""
            else:
                server = Server(
                    id=inst["id"],
                    name=inst.get("name", ""),
                    instance_type=inst.get("instanceType", ""),
                    status=inst.get("status", "pending"),
                    region=inst.get("region", ""),
                    ip_address=inst.get("ipAddress", ""),
                    cpu=spec.get("cpu", 0),
                    memory=spec.get("memory", 0),
                    disk=spec.get("disk", 0),
                    bandwidth=spec.get("bandwidth", 0),
                    charge_type=inst.get("chargeType", "PostPaid"),
                    user_id=int(current_user.id) if str(current_user.id).isdigit() else 1,
                )
                db.add(server)
            inst["remark"] = remark
        db.commit()
        return success(aliyun_instances)

    return success([])


@router.put("/{server_id}")
def update_server(server_id: str, body: dict = Body(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """更新服务器备注"""
    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        return error("服务器不存在", 404)
    if "remark" in body:
        server.remark = body["remark"]
    db.commit()
    return success({"id": server_id, "remark": server.remark})


@router.post("/{server_id}/start")
def start_server(server_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ok = start_ecs_instance(server_id)
    add_log(db, current_user.id, current_user.username, "start", "server", server_id,
            f"启动服务器 {server_id}", result="success" if ok else "failed")
    if not ok:
        return error("启动失败", 500)
    return success({"success": True}, "启动指令已发送")


@router.post("/{server_id}/stop")
def stop_server(server_id: str, body: dict = Body({"mode": "KeepCharging"}), db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    mode = body.get("mode", "KeepCharging")
    ok = stop_ecs_instance(server_id, mode)
    mode_label = "不收费" if mode == "StopCharging" else "收费"
    add_log(db, current_user.id, current_user.username, "stop", "server", server_id,
            f"停止服务器 {server_id}（{mode_label}）", result="success" if ok else "failed")
    if not ok:
        return error("停止失败", 500)
    return success({"success": True, "mode": mode}, "停止指令已发送")


@router.post("/{server_id}/release")
def release_server(server_id: str, current_user: User = Depends(get_current_user)):
    ok = delete_ecs_instance(server_id)
    if not ok:
        return error("释放失败", 500)
    return success({"success": True}, "实例已释放")


@router.get("/instance-types")
def list_instance_types(region: str = "", current_user: User = Depends(get_current_user)):
    """查询阿里云可用实例规格"""
    from app.aliyun_client import list_instance_types
    r = region or settings.ALIYUN_REGION
    return success(list_instance_types())


@router.get("/price")
def get_price(instanceType: str = "", region: str = "", current_user: User = Depends(get_current_user)):
    """查询按量实例价格"""
    from app.aliyun_client import get_instance_price
    r = region or settings.ALIYUN_REGION
    price = get_instance_price(instanceType, r)
    return success(price or {"price": 0})


@router.get("/resources")
def list_resources(region: str = "", current_user: User = Depends(get_current_user)):
    """查询镜像、安全组、交换机"""
    from app.aliyun_client import list_available_images, list_security_groups, list_vswitches
    r = region or settings.ALIYUN_REGION
    return success({
        "images": list_available_images(r),
        "securityGroups": list_security_groups(r),
        "vswitches": list_vswitches(r),
    })


@router.get("/{server_id}/metrics")
def get_metrics(server_id: str, current_user: User = Depends(get_current_user)):
    """获取 CPU/内存监控数据"""
    from app.aliyun_client import get_client
    from app.config import settings

    # Debug: check config
    print(f"[Metrics] AccessKey configured: {'yes' if settings.ALIYUN_ACCESS_KEY_ID else 'no'}")
    print(f"[Metrics] Server ID: {server_id}")

    client = get_client()
    if not client:
        print("[Metrics] No Aliyun client")
        return success({"cpu": None, "memory": None})

    def get_last(metric: str):
        try:
            req = DescribeMetricLastRequest.DescribeMetricLastRequest()
            req.set_Namespace("acs_ecs_dashboard")
            req.set_MetricName(metric)
            req.set_Dimensions(f'[{{"instanceId":"{server_id}"}}]')
            body = client.do_action_with_exception(req)
            data = json.loads(body)
            points = data.get("Datapoints", "")
            if points:
                items = json.loads(points)
                if items:
                    return round(items[-1].get("Average", 0), 1)
            return None
        except Exception as e:
            print(f"[Metrics] {metric} error: {e}")
            return None

    cpu_val = get_last("CPUUtilization")
    mem_val = get_last("memory_usedutilization")
    disk_val = get_last("diskusage_utilization")
    print(f"[Metrics] Result: cpu={cpu_val}, mem={mem_val}, disk={disk_val}")
    return success({"cpu": cpu_val, "memory": mem_val, "disk": disk_val})
