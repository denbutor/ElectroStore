from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.category import Category
from app.db.repositories.icategory_repository import ICategoryRepository


class CategoryRepository(ICategoryRepository):
    async def get_categories(self, db: AsyncSession) -> list[Category]:
        result = await db.execute(select(Category))
        return result.scalars().all()

    # async def get_category_with_products(self, db: AsyncSession, category_id: int) -> Category | None:
    #     result = await db.execute(
    #         select(Category).where(Category.id == category_id).options(selectinload(Category.products))
    #     )
    #     return result.scalars().first()

    async def get_category_with_products_by_name(self, db: AsyncSession, category_name: str) -> Category | None:
        result = await db.execute(
            select(Category)
            .where(Category.name == category_name)
            .options(selectinload(Category.products))  # Завантажуємо продукти
        )
        return result.scalars().first()




