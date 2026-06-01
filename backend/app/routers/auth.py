from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas.auth import LoginRequest
from app.utils.auth import hash_password, verify_password, create_access_token, get_current_user
from app.response import success, error

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.password_hash):
        return error("用户名或密码错误", 401)

    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return success({
        "token": token,
        "user": {
            "id": str(user.id),
            "username": user.username,
            "role": user.role.value,
            "avatar": user.username[0].upper(),
        },
    })


@router.get("/auth/me")
def get_me(current_user: User = Depends(get_current_user)):
    return success({
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role.value,
        "avatar": current_user.username[0].upper(),
    })
