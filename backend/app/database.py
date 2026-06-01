import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings

# Auto-create database with retries
base_url = settings.DATABASE_URL.rsplit("/", 1)[0]
db_name = settings.DATABASE_URL.rsplit("/", 1)[1].split("?")[0]
for attempt in range(10):
    try:
        engine = create_engine(base_url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            conn.commit()
        engine.dispose()
        print(f"[DB] MySQL ready ({db_name})")
        break
    except Exception as e:
        if attempt < 9:
            print(f"[DB] Waiting for MySQL ({attempt+1}/10): {e}")
            time.sleep(3)
        else:
            print(f"[ERROR] MySQL 连接失败: {e}")
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
