import logging
from fastapi import APIRouter, Depends, HTTPException
from kombu.asynchronous.http import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.core.database import get_db


logger = logging.getLogger("app")


router = APIRouter()


@router.post("", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):

    # 检查用户名是否已存在
    result = await db.execute(select(User).where(User.username == user.username))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # 创建新用户
    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    # 添加日志 用户 添加成功
    logger.info("User created successfully")
    return new_user


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, payload: UserUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.username is not None and payload.username != user.username:
        dup_check = await db.execute(
            select(User).where(User.username == payload.username, User.id != user_id)
        )
        if dup_check.scalar_one_or_none() is not None:
            raise HTTPException(status_code=400, detail="Username already registered")
        user.username = payload.username

    if payload.password is not None:
        user.password = payload.password

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"detail": "User deleted"}
