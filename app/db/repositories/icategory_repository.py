from abc import abstractmethod, ABC

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.category import Category


class ICategoryRepository(ABC):
    @abstractmethod
    async def get_categories(self, db: AsyncSession) -> list[Category]:
        pass

    @abstractmethod
    async def get_category_with_products_by_name(self, db: AsyncSession, category_name: str) -> Category | None:
        pass

