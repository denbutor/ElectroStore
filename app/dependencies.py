from app.db.session import get_db


async def get_db_dependency():
    async with get_db() as session:
        yield session