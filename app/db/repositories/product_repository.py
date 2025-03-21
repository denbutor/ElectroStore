from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.product import Product
from app.db.repositories.iproduct_repository import IProductRepository
from app.db.schemas.product import ProductCreate
from app.factories.product_factory import ProductFactory

#-----------------------------------------------------------------------
# First Version !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#-----------------------------------------------------------------------
# class ProductRepository(IProductRepository):
#     async def create_product(self, db: AsyncSession, product_data: ProductCreate) -> Product:
#         new_product = ProductFactory(**product_data.model_dump())
#         db.add(new_product)
#         await db.commit()
#         await db.refresh(new_product)
#         return new_product
#
#     async def get_products(self, db: AsyncSession) -> list[Product]:
#         result = await db.execute(select(Product))
#         return result.scalars().all()
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# First GPT Version !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#-----------------------------------------------------------------------
class ProductRepository(IProductRepository):
    async def create_product(self, db: AsyncSession, product_data: ProductCreate) -> Product:
        new_product = Product(**product_data.model_dump())
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        return new_product

    async def get_products(self, db: AsyncSession):
        result = await db.execute(select(Product))
        return result.scalars().all()
# -----------------------------------------------------------------------