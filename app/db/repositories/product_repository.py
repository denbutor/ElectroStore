from app.exceptions import ProductNotFoundException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.product import Product
from app.db.repositories.iproduct_repository import IProductRepository
from app.db.schemas.product import ProductCreate, ProductUpdate


class ProductRepository(IProductRepository):
    async def create_product(self, db: AsyncSession, product_data: ProductCreate) -> Product:
        new_product = Product(**product_data.model_dump())
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        return new_product



    async def update_product(self, db: AsyncSession, product, product_data: ProductUpdate) -> Product | None:
        result = await db.execute(select(Product).where(Product.id == product.id).where(Product.id == product.id))
        product = result.scalar_one_or_none()
        if not product:
            raise ProductNotFoundException()
        for field, value in product_data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        await db.commit()
        await db.refresh(product)
        return product

    async def delete_product(self, db: AsyncSession, product_id: int) -> bool:
        result = await db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            return False
        await db.delete(product)
        await db.commit()
        return True

    async def get_products(self, db: AsyncSession):
        result = await db.execute(select(Product))
        return result.scalars().all()

    async def get_product_by_name(self, db: AsyncSession, name: str) -> Product | None:
        result = await db.execute(select(Product).where(Product.name == name))
        return result.scalars().first()

    async def search_products_by_name(self, db: AsyncSession, name: str) -> list[Product]:
        result = await db.execute(select(Product).where(Product.name.ilike(f"%{name}%")))
        return result.scalars().all()

    async def get_product_by_id(self, db: AsyncSession, product_id: int) -> Product:
        result = await db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            raise ProductNotFoundException()
        return product