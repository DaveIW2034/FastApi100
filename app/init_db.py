import asyncio
from app.core.database import engine
from app.models import user  # 确保导入了模型
from app.core.database import Base

async def init_models():
    """Initialize database models by creating all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database models initialized successfully!")

if __name__ == "__main__":
    print("Initializing database models...")
    asyncio.run(init_models())
