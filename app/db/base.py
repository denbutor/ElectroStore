from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


# Base: DeclarativeMeta = declarative_base()
#
# engine: AsyncEngine = create_async_engine(settings.DATABASE_URL, echo=True)
#
# AsyncSessionLocal = async_sessionmaker(
#     bind=engine,
#     expire_on_commit=False,
#     class_=AsyncSession
# )

Base = declarative_base()

# Асинхронний двигун
async_engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Фабрика асинхронних сесій
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Депенденсі для отримання сесії БД
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session