from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.category import Category


class ICategoryRepository(ABC):
    @abstractmethod
    async def get_categories(self, db: AsyncSession) -> list[Category]:
        pass