from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.db.base import engine

async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with async_session() as session:
        yield session
