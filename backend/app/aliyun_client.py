import json
import logging
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import (
    DescribeInstancesRequest,
    StartInstanceRequest,
    StopInstanceRequest,
)
from app.config import settings

logger = logging.getLogger(__name__)


def get_client() -> AcsClient | None:
    key = settings.ALIYUN_ACCESS_KEY_ID
    secret = settings.ALIYUN_ACCESS_KEY_SECRET
    region = settings.ALIYUN_REGION
    if not key or not secret:
        logger.warning("阿里云 AccessKey 未配置，无法调用云 API")
        return None
    return AcsClient(key, secret, region)


def list_ecs_instances() -> list[dict]:
    """从阿里云拉取 ECS 实例列表"""
    client = get_client()
    if not client:
        return []

    req = DescribeInstancesRequest.DescribeInstancesRequest()
    req.set_PageSize(100)

    try:
        body = client.do_action_with_exception(req)
        data = json.loads(body)
        instances = []
        for inst in data.get("Instances", {}).get("Instance", []):
            instances.append({
                "id": inst.get("InstanceId"),
                "name": inst.get("InstanceName", f"ECS-{inst.get('InstanceId')}"),
                "instance_type": inst.get("InstanceType"),
                "status": _map_status(inst.get("Status")),
                "region": inst.get("RegionId"),
                "ip_address": inst.get("PublicIpAddress", {}).get("IpAddress", [None])[0]
                or inst.get("PrivateIpAddress", {}).get("IpAddress", [None])[0],
                "cpu": inst.get("Cpu", 0),
                "memory": inst.get("Memory", 0),
                "disk": 40,
                "bandwidth": inst.get("InternetMaxBandwidthOut", 0),
                "charge_type": "PostPaid" if inst.get("ChargeType") == "PostPaid" else "PrePaid",
                "created_at": inst.get("CreationTime"),
                "expired_at": inst.get("ExpiredTime"),
            })
        return instances
    except Exception as e:
        logger.error(f"拉取 ECS 列表失败: {e}")
        return []


def start_ecs_instance(instance_id: str) -> bool:
    client = get_client()
    if not client:
        return False
    try:
        req = StartInstanceRequest.StartInstanceRequest()
        req.set_InstanceId(instance_id)
        client.do_action_with_exception(req)
        return True
    except Exception as e:
        logger.error(f"启动 ECS {instance_id} 失败: {e}")
        return False


def stop_ecs_instance(instance_id: str) -> bool:
    client = get_client()
    if not client:
        return False
    try:
        req = StopInstanceRequest.StopInstanceRequest()
        req.set_InstanceId(instance_id)
        client.do_action_with_exception(req)
        return True
    except Exception as e:
        logger.error(f"停止 ECS {instance_id} 失败: {e}")
        return False


def _map_status(aliyun_status: str) -> str:
    mapping = {
        "Running": "running",
        "Stopped": "stopped",
        "Starting": "starting",
        "Stopping": "stopping",
        "Pending": "pending",
    }
    return mapping.get(aliyun_status, "error")
