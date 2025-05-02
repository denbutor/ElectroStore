from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.category_repository import CategoryRepository
from app.db.schemas.category import CategoryCreate, CategoryResponse
from app.db.schemas.product import ProductResponse
from app.exceptions import CategoryNotFoundException
from app.services.caches.category_cache import cache_category_products_by_name, cache_categories, get_cached_categories, \
    get_cached_category_products_by_name


class CategoryService:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def get_categories(self, db: AsyncSession) -> list[CategoryResponse]:
        cached = await get_cached_categories()
        if cached:
            return cached
        categories = await self.category_repo.get_categories(db)
        category_schemas = [
            CategoryResponse.model_validate(category) for category in categories
        ]
        await cache_categories(category_schemas)
        return category_schemas

    async def get_category_products_by_name(self, db: AsyncSession, category_name: str) -> list[ProductResponse]:
        cached = await get_cached_category_products_by_name(category_name)
        if cached:
            return cached

        category = await self.category_repo.get_category_with_products_by_name(db, category_name)
        if not category:
            raise CategoryNotFoundException()

        # Кешуємо товари
        await cache_category_products_by_name(category_name, category.products)

        return [
            ProductResponse.model_validate(product)
            for product in category.products
        ]


# class CategoryService:
#     def __init__(self, category_repo: CategoryRepository):
#         self.category_repo = category_repo
#
#     async def get_categories(self, db:AsyncSession):
#         return await self.category_repo.get_categories(db)
#
#     # async def get_category_products(self, db: AsyncSession, category_id: int):
#     #     category = await self.category_repo.get_category_with_products(db, category_id)
#     #     if not category:
#     #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
#     #     return category.products
#
#     async def get_category_products_by_name(self, db: AsyncSession, category_name: str):
#         category = await self.category_repo.get_category_with_products_by_name(db, category_name)
#         if not category:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
#         return category.products
