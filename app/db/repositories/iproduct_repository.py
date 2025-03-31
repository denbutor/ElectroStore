from abc import abstractmethod, ABC

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.product import Product
from app.db.schemas.product import ProductCreate, ProductUpdate


class IProductRepository(ABC):
    @abstractmethod
    async def create_product(self, db: AsyncSession, product_data: ProductCreate) -> Product:
        pass

    @abstractmethod
    async def get_products(self, db: AsyncSession) -> list[Product]:
        pass

    @abstractmethod
    async def update_product(self, db: AsyncSession, product, product_data: ProductUpdate):
        pass

    @abstractmethod
    async def delete_product(self, db: AsyncSession, product_id: int) -> bool:
        pass

    @abstractmethod
    async def get_product_by_name(self, db: AsyncSession, name: str) -> Product | None:
        pass

    @abstractmethod
    async def search_products_by_name(self, db: AsyncSession, name: str) -> list[Product]:
        pass

    @abstractmethod
    async def get_product_by_id(self, db: AsyncSession, product_id: int) -> Product:
        pass