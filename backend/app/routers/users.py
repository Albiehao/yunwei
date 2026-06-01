from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User
from app.schemas.user import UserOut, UserCreate, UserUpdate
from app.utils.auth import hash_password, get_current_user, require_admin
from app.response import success, error

router = APIRouter(prefix="/api/users", tags=["用户管理"])


@router.get("")
def list_users(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    users = db.query(User).all()
    return success(users)


@router.post("")
def create_user(data: UserCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    existing = db.query(User).filter((User.username == data.username) | (User.email == data.email)).first()
    if existing:
        return error("用户名或邮箱已存在", 400)
    user = User(
        username=data.username,
        email=data.email,
        phone=data.phone,
        password_hash=hash_password(data.password),
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return success(user)


@router.put("/{user_id}")
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return error("用户不存在", 404)
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(user, key, val)
    db.commit()
    db.refresh(user)
    return success(user)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    if user_id == current_user.id:
        return error("不能删除自己", 400)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return error("用户不存在", 404)
    db.delete(user)
    db.commit()
    return success(None, "删除成功")
