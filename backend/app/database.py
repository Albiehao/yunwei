from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.exc import OperationalError

from app.config import settings


def ensure_database():
    """Auto-create database if it doesn't exist"""
    base_url = settings.DATABASE_URL.rsplit("/", 1)[0]
    db_name = settings.DATABASE_URL.rsplit("/", 1)[1].split("?")[0]
    try:
        engine = create_engine(base_url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            conn.commit()
        engine.dispose()
    except Exception as e:
        print(f"[DB] Auto-create database skipped: {e}")


ensure_database()

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
