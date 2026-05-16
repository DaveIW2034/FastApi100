import pytest
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, engine


@pytest.mark.asyncio
async def test_connection_pool_basic():
    """
    测试连接池是否可以复用连接，并能正确连接数据库。
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1


@pytest.mark.asyncio
async def test_connection_pool_concurrent():
    """
    并发请求多个连接，确保连接池不会报错。
    """

    async def run_query(index: int):
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT SLEEP(0.1)"))  # 模拟数据库开销
            return result

    # 并发 15 个请求（可根据 pool_size + max_overflow 调整）
    tasks = [run_query(i) for i in range(15)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 检查是否所有任务都成功执行
    for res in results:
        if isinstance(res, Exception):
            raise res
