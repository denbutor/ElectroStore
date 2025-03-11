from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.product_repository import ProductRepository
from app.db.schemas.product import ProductCreate
from app.decorators.admin_decorator import requires_admin


class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    @requires_admin
    async def create(self, db: AsyncSession, product_data: ProductCreate):
        return await self.product_repo.create_product(db, product_data)

    async def get_products(self, db: AsyncSession):
        return await self.product_repo.get_products(db)