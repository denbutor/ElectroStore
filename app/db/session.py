from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.db.base import async_engine, AsyncSessionLocal

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
