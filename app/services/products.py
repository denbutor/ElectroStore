import json

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import redis
from app.core.redis import get_redis
from app.db.models.product import Product
from app.db.repositories.product_repository import ProductRepository
from app.db.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.db.schemas.user import UserResponse
from app.decorators.admin_decorator import requires_admin
from app.exceptions import ForbiddenException
from app.services.caches.product_cache import cache_product, CACHE_PREFIX


class ProductService:

    def __init__(self, product_repo: ProductRepository, redis_client: Redis):
        self.product_repo = product_repo
        self.redis_client = redis_client
        self.cache_prefix = "product:"

    async def create_product(self, db: AsyncSession, product_data: ProductCreate) -> ProductResponse:
        new_product = await self.product_repo.create_product(db, product_data)
        product_response = ProductResponse.model_validate(new_product)
        await cache_product(product_response)
        return product_response

    async def update_product(self, db: AsyncSession, product_id: int, product_data: ProductUpdate) -> ProductResponse | None:
        product = await self.product_repo.get_product_by_id(db, product_id)
        if not product:
            return None

        updated_product = await self.product_repo.update_product(db, product, product_data)
        return ProductResponse.model_validate(updated_product)

    async def delete_product(self, db: AsyncSession, product_id: int) -> bool:
        return await self.product_repo.delete_product(db, product_id)

    # async def update_product(self, db: AsyncSession, product_id: int, product_data: ProductUpdate) -> ProductResponse | None:
    #     product = await self.product_repo.get_product_by_id(db, product_id)
    #     if not product:
    #         return None
    #
    #     for field, value in product_data.model_dump(exclude_unset=True).items():
    #         setattr(product, field, value)
    #
    #     await db.commit()
    #     await db.refresh(product)
    #     return ProductResponse.model_validate(product)
    #
    # async def delete_product(self, db: AsyncSession, product_id: int) -> bool:
    #     product = await self.product_repo.get_product_by_id(db, product_id)
    #     if not product:
    #         return False
    #     await db.delete(product)
    #     await db.commit()
    #     return True



    async def get_products(self, db: AsyncSession):
        return await self.product_repo.get_products(db)

    async def get_product_by_name(self, db: AsyncSession, name: str) -> ProductResponse | None:
        product = await self.product_repo.get_product_by_name(db, name)
        if not product:
            return None
        return ProductResponse.model_validate(product)

    async def search_products_by_name(self, db: AsyncSession, name: str) -> list[ProductResponse]:
        products = await self.product_repo.search_products_by_name(db, name)
        return [ProductResponse.model_validate(product) for product in products]


