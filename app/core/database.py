# -*- coding: utf-8 -*-
"""
文件: database.py
说明: 初始化 SQLAlchemy 异步引擎与会话工厂，提供 FastAPI 依赖 `get_db`。
创建时间: 2025-08-19
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.mysql_config import DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 最大溢出连接数
    pool_timeout=30,  # 连接池超时时间
    pool_recycle=1800,  # 连接回收时间
)

# ✅ 定义这个变量：
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session

