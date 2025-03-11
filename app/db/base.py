from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine,AsyncSession
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


Base: DeclarativeMeta = declarative_base()

engine: AsyncEngine = create_async_engine(settings.DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)