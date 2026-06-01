import os
import time
import threading
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import engine, Base, SessionLocal
from app.models import User, UserRole, UserStatus
from app.models.server import Server, ServerStatus
from app.models.schedule import Schedule, ScheduleAction
from app.models.task import Task
from app.models.log import Log
from app.utils.auth import hash_password
from app.aliyun_client import start_ecs_instance, stop_ecs_instance
from app.utils.log import add_log

logger = logging.getLogger(__name__)


def init_db():
    """Create tables, migrate columns, and seed default admin user"""
    Base.metadata.create_all(bind=engine)
    # Migrate columns
    from sqlalchemy import text, inspect
    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE servers ADD COLUMN remark VARCHAR(200)"))
            conn.commit()
            print("[DB] Added remark column")
    except Exception:
        pass
    db = SessionLocal()
    try:
        # Recreate admin user
        db.query(User).delete()
        admin = User(
            username="albieAdmin",
            email="admin@xuntianops.com",
            password_hash=hash_password("ZjhXhxy1999"),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
        )
        db.add(admin)

        db.commit()
        print("[DB] Admin user seeded")
    finally:
        db.close()


def run_scheduler():
    """Background scheduler: check every 60s for tasks to execute"""
    while True:
        try:
            db = SessionLocal()
            now = time.localtime()
            schedules = db.query(Schedule).filter(Schedule.enabled == True).all()
            for s in schedules:
                parts = s.cron_expression.strip().split()
                if len(parts) != 5:
                    continue
                minute, hour, dom, month, dow = parts
                match = True
                if minute != "*" and str(now.tm_min) not in minute.split(","):
                    match = False
                if hour != "*" and str(now.tm_hour) not in hour.split(","):
                    match = False
                if dom != "*" and str(now.tm_mday) not in dom.split(","):
                    match = False
                if month != "*" and str(now.tm_mon) not in month.split(","):
                    match = False
                if dow != "*" and str(now.tm_wday) not in dow.split(","):
                    match = False
                if match:
                    server = db.query(Server).filter(Server.id == s.server_id).first()
                    inst_id = s.server_id
                    action_name = "start" if s.action == ScheduleAction.START else "stop"
                    if s.action == ScheduleAction.START:
                        ok = start_ecs_instance(inst_id)
                    else:
                        ok = stop_ecs_instance(inst_id, "KeepCharging")
                    add_log(db, user_id=s.user_id or 0, username="scheduler",
                            action=action_name, target_type="server", target_id=inst_id,
                            detail=f"定时{action_name} {inst_id}", result="success" if ok else "failed")
                    if ok:
                        if server:
                            server.status = ServerStatus.RUNNING if s.action == ScheduleAction.START else ServerStatus.STOPPED
                        s.last_run_at = __import__("datetime").datetime.utcnow()
                        db.commit()
            db.close()
        except Exception as e:
            print(f"[Scheduler] Error: {e}")
        time.sleep(60)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    t = threading.Thread(target=run_scheduler, daemon=True)
    t.start()
    print("[Scheduler] Started")
    yield


app = FastAPI(
    title="寻天运维平台 API",
    description="云服务器运维管理后端接口",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
from app.routers import auth, servers, schedules, users, ssh, tasks, logs
app.include_router(auth.router)
app.include_router(servers.router)
app.include_router(schedules.router)
app.include_router(users.router)
app.include_router(ssh.router)
app.include_router(tasks.router)
app.include_router(logs.router)


# Serve frontend static files in production
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_dist = os.path.join(_root, "dist")
if os.path.isdir(frontend_dist):
    # Mount static assets
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    # SPA fallback: all non-API routes → index.html
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api/"):
            from fastapi.responses import JSONResponse
            return JSONResponse({"detail": "Not Found"}, status_code=404)
        file_path = os.path.join(frontend_dist, "index.html")
        if os.path.isfile(file_path):
            return FileResponse(file_path, media_type="text/html")
        return JSONResponse({"detail": "Not Found"}, status_code=404)
else:
    @app.get("/")
    def root():
        return {"name": "寻天运维平台 API", "version": "1.0.0"}
