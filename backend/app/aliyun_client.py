import json
import logging
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import (
    DescribeInstancesRequest,
    StartInstanceRequest,
    StopInstanceRequest,
    DeleteInstanceRequest,
    DescribeInstanceTypesRequest,
    CreateInstanceRequest,
    AllocatePublicIpAddressRequest,
    DescribeImagesRequest,
    DescribeSecurityGroupsRequest,
    DescribeVSwitchesRequest,
    DescribePriceRequest,
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


def list_ecs_instances(region_override: str = "") -> list[dict]:
    """从阿里云拉取 ECS 实例列表"""
    client = get_client()
    if not client:
        return []

    if region_override:
        client.set_region_id(region_override)

    req = DescribeInstancesRequest.DescribeInstancesRequest()
    req.set_PageSize(100)

    try:
        body = client.do_action_with_exception(req)
        data = json.loads(body)
        instances = data.get("Instances", {}).get("Instance", [])
        print(f"[Aliyun] Region: {client.get_region_id()}, Found {len(instances)} ECS instance(s)")
        result = []
        for inst in instances:
            ip_list = inst.get("PublicIpAddress", {}).get("IpAddress", [])
            if not ip_list:
                ip_list = inst.get("PrivateIpAddress", {}).get("IpAddress", [])
            ip = ip_list[0] if ip_list else ""
            raw_charge = inst.get("ChargeType", "")
            charge_type = "PostPaid" if raw_charge.lower() != "prepaid" else "PrePaid"
            print(f"[Aliyun]   ChargeType raw='{raw_charge}' -> '{charge_type}'")
            raw_mem = inst.get("Memory", 0)
            mem_gb = raw_mem // 1024 if raw_mem > 1024 else raw_mem  # Aliyun returns MB, convert to GB
            info = {
                "id": inst.get("InstanceId"),
                "name": inst.get("InstanceName", f"ECS-{inst.get('InstanceId')}"),
                "instanceType": inst.get("InstanceType"),
                "status": _map_status(inst.get("Status")),
                "region": inst.get("RegionId"),
                "ipAddress": ip or "",
                "spec": {
                    "cpu": inst.get("Cpu", 0),
                    "memory": mem_gb,
                    "disk": 40,
                    "bandwidth": inst.get("InternetMaxBandwidthOut", 0),
                },
                "chargeType": charge_type,
                "createdAt": inst.get("CreationTime"),
                "expiredAt": inst.get("ExpiredTime"),
            }
            print(f"[Aliyun]   - {info['id']} | {info['name']} | {info['status']} | {info['ipAddress'] or '无IP'}")
            result.append(info)
        return result
    except Exception as e:
        print(f"[Aliyun] ERROR: 拉取ECS列表失败: {e}")
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


def delete_ecs_instance(instance_id: str) -> bool:
    """释放按量付费实例"""
    client = get_client()
    if not client:
        return False
    try:
        req = DeleteInstanceRequest.DeleteInstanceRequest()
        req.set_InstanceId(instance_id)
        req.set_Force(True)
        client.do_action_with_exception(req)
        print(f"[Aliyun] Released instance: {instance_id}")
        return True
    except Exception as e:
        print(f"[Aliyun] 释放 {instance_id} 失败: {e}")
        return False


def stop_ecs_instance(instance_id: str, mode: str = "KeepCharging") -> bool:
    client = get_client()
    if not client:
        return False
    try:
        req = StopInstanceRequest.StopInstanceRequest()
        req.set_InstanceId(instance_id)
        if mode == "StopCharging":
            req.set_StoppedMode("StopCharging")
        client.do_action_with_exception(req)
        print(f"[Aliyun] Stopped {instance_id} mode={mode}")
        return True
    except Exception as e:
        print(f"[Aliyun] 停止 {instance_id} 失败: {e}")
        return False


def list_available_images(region: str = "") -> list[dict]:
    """查询可用镜像"""
    client = get_client()
    if not client:
        return []
    if region:
        client.set_region_id(region)
    try:
        req = DescribeImagesRequest.DescribeImagesRequest()
        req.set_Status("Available")
        body = client.do_action_with_exception(req)
        data = json.loads(body)
        images = data.get("Images", {}).get("Image", [])
        return [{
            "id": img.get("ImageId", ""),
            "name": img.get("ImageName", ""),
            "osName": img.get("OSName", ""),
            "size": img.get("Size", 0),
        } for img in images[:20]]
    except Exception as e:
        print(f"[Aliyun] 查询镜像失败: {e}")
        return []


def list_security_groups(region: str = "") -> list[dict]:
    """查询安全组"""
    client = get_client()
    if not client:
        return []
    if region:
        client.set_region_id(region)
    try:
        req = DescribeSecurityGroupsRequest.DescribeSecurityGroupsRequest()
        body = client.do_action_with_exception(req)
        data = json.loads(body)
        groups = data.get("SecurityGroups", {}).get("SecurityGroup", [])
        return [{"id": g.get("SecurityGroupId", ""), "name": g.get("SecurityGroupName", "")} for g in groups]
    except Exception as e:
        print(f"[Aliyun] 查询安全组失败: {e}")
        return []


def list_vswitches(region: str = "") -> list[dict]:
    """查询交换机"""
    client = get_client()
    if not client:
        return []
    if region:
        client.set_region_id(region)
    try:
        req = DescribeVSwitchesRequest.DescribeVSwitchesRequest()
        body = client.do_action_with_exception(req)
        data = json.loads(body)
        vs = data.get("VSwitches", {}).get("VSwitch", [])
        return [{"id": v.get("VSwitchId", ""), "name": v.get("VSwitchName", "")} for v in vs]
    except Exception as e:
        print(f"[Aliyun] 查询交换机失败: {e}")
        return []


def get_instance_price(instance_type: str, region: str) -> dict | None:
    """查询按量实例价格"""
    client = get_client()
    if not client:
        return None
    if region:
        client.set_region_id(region)
    try:
        req = DescribePriceRequest.DescribePriceRequest()
        req.set_ResourceType("instance")
        req.set_InstanceType(instance_type)
        req.set_PriceUnit("Hour")
        req.set_Period(1)
        body = client.do_action_with_exception(req)
        data = json.loads(body)
        print(f"[Price] raw: {json.dumps(data, ensure_ascii=False)[:300]}")
        info = data.get("PriceInfo", {})
        price = info.get("TradePrice") or info.get("Price", {}).get("TradePrice") or 0
        return {
            "price": round(float(price), 4),
            "currency": info.get("Currency", "CNY") or "CNY",
        }
    except Exception as e:
        print(f"[Aliyun] 查询价格失败: {e}")
        return None


def fetch_instance_prices(instance_types: list[dict], region: str) -> list[dict]:
    """批量查询价格并合并到实例规格中"""
    result = []
    for t in instance_types:
        price = get_instance_price(t["id"], region)
        result.append({
            **t,
            "price": price["hourly"] if price else 0,
            "currency": price["currency"] if price else "CNY",
        })
    return result


def list_instance_types() -> list[dict]:
    """获取可用实例规格"""
    client = get_client()
    if not client:
        return []
    try:
        req = DescribeInstanceTypesRequest.DescribeInstanceTypesRequest()
        body = client.do_action_with_exception(req)
        data = json.loads(body)
        types = data.get("InstanceTypes", {}).get("InstanceType", [])
        result = []
        for t in types[:20]:  # top 20
            result.append({
                "id": t.get("InstanceTypeId", ""),
                "cpu": t.get("CpuCoreCount", 0),
                "memory": t.get("MemorySize", 0),
                "family": t.get("InstanceTypeFamily", ""),
            })
        return result
    except Exception as e:
        print(f"[Aliyun] 查询实例规格失败: {e}")
        return []


def create_ecs_instance(instance_type: str, region: str, image_id: str = "centos_8_5_x64_20G_alibase_20211129.vhd") -> str | None:
    """创建按量付费实例，返回 instance_id"""
    client = get_client()
    if not client:
        return None
    try:
        req = CreateInstanceRequest.CreateInstanceRequest()
        req.set_InstanceType(instance_type)
        req.set_RegionId(region)
        req.set_ImageId(image_id)
        req.set_ChargeType("PostPaid")
        req.set_InstanceChargeType("PostPaid")
        req.set_InternetChargeType("PayByTraffic")
        req.set_InternetMaxBandwidthOut(100)
        req.set_SecurityGroupId("sg-bp1hv4sqs1x1n1x1xxxx")  # user needs to set this
        req.set_VSwitchId("vsw-bp1xxxxx")  # user needs to set this
        body = client.do_action_with_exception(req)
        data = json.loads(body)
        instance_id = data.get("InstanceId")
        if instance_id:
            # Allocate public IP
            try:
                ip_req = AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest()
                ip_req.set_InstanceId(instance_id)
                client.do_action_with_exception(ip_req)
            except:
                pass
            return instance_id
        return None
    except Exception as e:
        print(f"[Aliyun] 创建实例失败: {e}")
        return None


def _map_status(aliyun_status: str) -> str:
    mapping = {
        "Running": "running",
        "Stopped": "stopped",
        "Starting": "starting",
        "Stopping": "stopping",
        "Pending": "pending",
    }
    return mapping.get(aliyun_status, "error")
