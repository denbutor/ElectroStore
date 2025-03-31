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

    async def update_product(self, db: AsyncSession, product_id: int,
                             update_data: ProductUpdate) -> ProductResponse | None:
        product = await self.product_repo.update_product(db, product_id, update_data)
        if not product:
            return None
        product_response = ProductResponse.model_validate(product)
        await cache_product(product_response)
        return product_response

    async def delete_product(self, db: AsyncSession, product_id: int) -> bool:
        deleted = await self.product_repo.delete_product(db, product_id)
        if deleted:
            redis_client = await get_redis()
            await redis_client.delete(f"{CACHE_PREFIX}{product_id}")
        return deleted

    # @requires_admin
    # async def create_product(
    #         self, db: AsyncSession,
    #         product_data: ProductCreate,
    #         current_user: UserResponse,
    # ) -> ProductResponse:
    #     if current_user.role != "admin":
    #         raise ForbiddenException(detail="Insufficient privileges")
    #     new_product = await self.product_repo.create_product(db, product_data)
    #     return ProductResponse.model_validate(new_product)
    #
    # @requires_admin
    # async def update_product(self, db: AsyncSession, product_id: int, updated_data: ProductUpdate) -> ProductResponse:
    #     product = await self.product_repo.update_product(db, product_id, updated_data)
    #     return ProductResponse.model_validate(product)
    #
    # @requires_admin
    # async def delete_product(self, db: AsyncSession, product_id: int):
    #     await self.product_repo.delete_product(db, product_id)

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


