from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import engine, Base, SessionLocal
from app.models import User, UserRole, UserStatus
from app.models.server import Server
from app.models.schedule import Schedule
from app.models.task import Task
from app.utils.auth import hash_password
import os


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


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
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
