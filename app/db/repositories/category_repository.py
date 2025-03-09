from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.category import Category
from app.db.repositories.icategory_repository import ICategoryRepository


class CategoryRepository(ICategoryRepository):
    async def get_categories(self, db: AsyncSession) -> list[Category]:
        result = await db.execute(select(Category))
        return result.scalars().all()