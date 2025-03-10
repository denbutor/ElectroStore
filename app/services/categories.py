from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.category_repository import CategoryRepository
from app.db.schemas.category import CategoryCreate


class CategoryService:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def create_category(self, db:AsyncSession, category_data: CategoryCreate):
        return await self.category_repo(db,category_data)

    async def get_categories(self, db:AsyncSession):
        return await self.category_repo.get_categories(db)