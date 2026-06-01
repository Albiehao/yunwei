import paramiko
from fastapi import APIRouter, Body
from app.response import success, error

router = APIRouter(prefix="/api/ssh", tags=["SSH"])
_sessions = {}
_counter = 0


@router.post("/connect")
def connect(body: dict = Body(...)):
    host = body.get("host", "")
    user = body.get("username", "root")
    passwd = body.get("password", "")
    port = body.get("port", 22)

    if not host:
        return error("主机不能为空", 400)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if passwd:
            ssh.connect(host, port=port, username=user, password=passwd, timeout=15, banner_timeout=10)
        else:
            ssh.connect(host, port=port, username=user, timeout=15, banner_timeout=10, look_for_keys=True, allow_agent=True)
    except paramiko.AuthenticationException:
        return error("认证失败，请检查用户名密码", 401)
    except Exception as e:
        return error(f"连接失败: {e}", 502)

    global _counter
    _counter += 1
    sid = f"s{_counter}"
    _sessions[sid] = {"client": ssh, "host": host, "user": user}
    return success({"id": sid})


@router.post("/exec")
def exec_cmd(body: dict = Body(...)):
    sid = body.get("id", "")
    cmd = body.get("command", "")
    sess = _sessions.get(sid)
    if not sess:
        return error("会话已过期", 404)
    if not cmd:
        return error("命令为空", 400)
    try:
        ssh: paramiko.SSHClient = sess["client"]
        _, stdout, stderr = ssh.exec_command(cmd, timeout=30)
        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        rc = stdout.channel.recv_exit_status()
        return success({"output": out + err, "exit_code": rc})
    except Exception as e:
        return error(f"执行失败: {e}", 500)


@router.post("/disconnect")
def disconnect(body: dict = Body(...)):
    sid = body.get("id", "")
    sess = _sessions.pop(sid, None)
    if sess:
        try:
            sess["client"].close()
        except:
            pass
    return success(None, "已断开")
