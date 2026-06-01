from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User
from app.models.server import Server, ServerStatus
from app.schemas.server import ServerOut, ServerActionResponse
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/servers", tags=["服务器"])


@router.get("", response_model=List[ServerOut])
def list_servers(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    servers = db.query(Server).filter(Server.user_id == current_user.id).all()
    return servers


@router.post("/{server_id}/start", response_model=ServerActionResponse)
def start_server(server_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    server = db.query(Server).filter(Server.id == server_id, Server.user_id == current_user.id).first()
    if not server:
        raise HTTPException(status_code=404, detail="服务器不存在")
    if server.status == ServerStatus.RUNNING:
        return ServerActionResponse(success=True, message="服务器已运行")

    server.status = ServerStatus.STARTING
    db.commit()
    # 模拟异步：实际会调用云API
    import threading, datetime
    def _start():
        import time
        time.sleep(2)
        from app.database import SessionLocal
        s = SessionLocal()
        svr = s.query(Server).filter(Server.id == server_id).first()
        if svr:
            svr.status = ServerStatus.RUNNING
            s.commit()
        s.close()
    threading.Thread(target=_start, daemon=True).start()
    return ServerActionResponse(success=True, message="启动指令已发送")


@router.post("/{server_id}/stop", response_model=ServerActionResponse)
def stop_server(server_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    server = db.query(Server).filter(Server.id == server_id, Server.user_id == current_user.id).first()
    if not server:
        raise HTTPException(status_code=404, detail="服务器不存在")
    if server.status == ServerStatus.STOPPED:
        return ServerActionResponse(success=True, message="服务器已停止")

    server.status = ServerStatus.STOPPING
    db.commit()
    import threading
    def _stop():
        import time
        time.sleep(2)
        from app.database import SessionLocal
        s = SessionLocal()
        svr = s.query(Server).filter(Server.id == server_id).first()
        if svr:
            svr.status = ServerStatus.STOPPED
            s.commit()
        s.close()
    threading.Thread(target=_stop, daemon=True).start()
    return ServerActionResponse(success=True, message="停止指令已发送")
