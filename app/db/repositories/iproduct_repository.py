from abc import abstractmethod, ABC

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.product import Product


class IProductRepository(ABC):
    @abstractmethod
    async def create_product(self, db: AsyncSession, product_data: ProductCreate) -> Product:
        pass

    @abstractmethod
    async def get_products(self, db: AsyncSession) -> list[Product]:
        pass