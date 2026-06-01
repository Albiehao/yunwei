from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings

# Auto-create database if not exists
base_url = settings.DATABASE_URL.rsplit("/", 1)[0]
db_name = settings.DATABASE_URL.rsplit("/", 1)[1].split("?")[0]
try:
    engine = create_engine(base_url, pool_pre_ping=True)
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
        conn.commit()
    engine.dispose()
except Exception as e:
    print(f"[ERROR] 无法连接 MySQL: {e}")
    print("[ERROR] 请确保 MySQL 已启动，或检查 backend/.env 中的 DATABASE_URL 配置")
    raise

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
