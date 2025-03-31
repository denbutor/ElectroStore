from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.product import Product
from app.db.repositories.iproduct_repository import IProductRepository
from app.db.schemas.product import ProductCreate, ProductUpdate
from app.factories.product_factory import ProductFactory
from sqlalchemy.orm import Session
from app.core.security import get_current_user

from app.db.schemas.product import ProductCreate, ProductUpdate


# class ProductRepository:
#     @staticmethod
#     def create_product(db: Session, product_data: ProductCreate) -> Product:
#         new_product = Product(**product_data.model_dump())
#         db.add(new_product)
#         db.commit()
#         db.refresh(new_product)
#         return new_product
#
#     @staticmethod
#     def get_product_by_id(db: Session, product_id: int) -> Product | None:
#         return db.query(Product).filter(Product.id == product_id).first()
#
#     @staticmethod
#     def update_product(db: Session, product_id: int, product_data: ProductUpdate) -> Product | None:
#         product = db.query(Product).filter(Product.id == product_id).first()
#         if not product:
#             return None
#
#         for key, value in product_data.model_dump(exclude_unset=True).items():
#             setattr(product, key, value)
#
#         db.commit()
#         db.refresh(product)
#         return product
#
#     @staticmethod
#     def delete_product(db: Session, product_id: int) -> bool:
#         product = db.query(Product).filter(Product.id == product_id).first()
#         if not product:
#             return False
#         db.delete(product)
#         db.commit()
#         return True
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.product import Product
from app.db.repositories.iproduct_repository import IProductRepository
from app.db.schemas.product import ProductCreate, ProductUpdate
from app.factories.product_factory import ProductFactory
from sqlalchemy.orm import Session
from app.core.security import get_current_user

from app.db.schemas.product import ProductCreate, ProductUpdate


class ProductRepository(IProductRepository):
    async def create_product(self, db: AsyncSession, product_data: ProductCreate) -> Product:
        new_product = Product(**product_data.model_dump())
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        return new_product

    async def update_product(self, db: AsyncSession, product, product_data: ProductUpdate):
        for field, value in product_data.dict(exclude_unset=True).items():
            setattr(product, field, value)
        await db.commit()
        await db.refresh(product)
        return product

    async def delete_product(self, db: AsyncSession, product_id: int) -> bool:
        product = await self.get_product_by_id(db, product_id)
        if not product:
            return False

        await db.delete(product)
        await db.commit()
        return True

    # async def delete_product(self, db: AsyncSession, name: str) -> bool:
    #     product = await self.get_product_by_name(db, name)
    #     if not product:
    #         return False
    #
    #     await db.delete(product)
    #     await db.commit()
    #     return True

    # async def update_product(self, db: AsyncSession, product_id: int, updated_data: ProductUpdate):
    #     # product = await db.get(Product, product_id)
    #     # if not product:
    #     #     raise NoResultFound("Product not found")
    #     product = await self.get_product_by_id(db, product_id)
    #     if not product:
    #         return None
    #     for field, value in updated_data.model_dump(exclude_unset=True).items():
    #         setattr(product, field, value)
    #     await db.commit()
    #     await db.refresh(product)
    #     return product
    #
    # # @staticmethod
    # async def delete_product(self, db: AsyncSession, product_id: int):
    #     product = await self.get_product_by_id(db, product_id)
    #     if not product:
    #         return False
    #     await db.delete(product)
    #     await db.commit()
    #     return True

    # @staticmethod
    async def get_products(self, db: AsyncSession):
        result = await db.execute(select(Product))
        return result.scalars().all()

    # @staticmethod
    async def get_product_by_name(self, db: AsyncSession, name: str) -> Product | None:
        result = await db.execute(select(Product).where(Product.name == name))
        return result.scalars().first()

    # @staticmethod
    async def search_products_by_name(self, db: AsyncSession, name: str) -> list[Product]:
        result = await db.execute(select(Product).where(Product.name.ilike(f"%{name}%")))
        return result.scalars().all()

    # @staticmethod
    async def get_product_by_id(self, db: AsyncSession, product_id: int) -> Product:
        result = await db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            raise NoResultFound("Product not found")
        return product

    # @staticmethod

# -----------------------------------------------------------------------
# class ProductRepository(IProductRepository):
#     async def create_product(self, db: AsyncSession, product_data: ProductCreate) -> Product:
#         new_product = Product(**product_data.model_dump())
#         db.add(new_product)
#         await db.commit()
#         await db.refresh(new_product)
#         return new_product
#
#     async def get_products(self, db: AsyncSession):
#         result = await db.execute(select(Product))
#         return result.scalars().all()
#
#     async def get_product_by_name(self, db: AsyncSession, name: str) -> Product | None:
#         result = await db.execute(select(Product).where(Product.name == name))
#         return result.scalars().first()
#
#     async def search_products_by_name(self, db: AsyncSession, name: str) -> list[Product]:
#         result = await db.execute(select(Product).where(Product.name.ilike(f"%{name}%")))
#         return result.scalars().all()
#
#     async def get_product_by_id(self, db: AsyncSession, product_id: int) -> Product:
#         result = await db.execute(select(Product).where(Product.id == product_id))
#         product = result.scalar_one_or_none()
#         if not product:
#             raise NoResultFound("Product not found")
#         return product
#
#     async def update_product(self, db: AsyncSession, product_id: int, updated_data: ProductUpdate):
#         product = await db.get(Product, product_id)
#         if not product:
#             raise NoResultFound("Product not found")
#
#         # for field, value in updated_data.model_dump(exclude_unset=True).items():
#         for field, value in updated_data.dict(exclude_unset=True).items():
#             setattr(product, field, value)
#
#         await db.commit()
#         await db.refresh(product)
#         return product
#
#     async def delete_product(self, db: AsyncSession, product_id: int):
#         product = await self.get_product_by_id(db, product_id)
#         await db.delete(product)
#         await db.commit()
# -----------------------------------------------------------------------