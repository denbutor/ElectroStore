from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.category_repository import CategoryRepository
from app.db.schemas.category import CategoryCreate


class CategoryService:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def get_categories(self, db:AsyncSession):
        return await self.category_repo.get_categories(db)

    # async def get_category_products(self, db: AsyncSession, category_id: int):
    #     category = await self.category_repo.get_category_with_products(db, category_id)
    #     if not category:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    #     return category.products

    async def get_category_products_by_name(self, db: AsyncSession, category_name: str):
        category = await self.category_repo.get_category_with_products_by_name(db, category_name)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return category.products
