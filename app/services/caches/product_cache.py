import json
import redis.asyncio as redis


from app.core.redis import get_redis
from app.db.models.product import Product
from app.db.schemas.product import ProductResponse

CACHE_EXPIRE = 60
CACHE_PREFIX = "product:"


# async def cache_products(products: list[Product]):
#     redis_client = await get_redis()
#     # products_data = [product.model_dump() for product in products]
#     products_data = [
#         ProductResponse.model_validate(product).model_dump(mode="json")
#         for product in products
#     ]
#     await redis_client.set("products_cache", json.dumps(products_data), ex=CACHE_EXPIRE)
#
#
# async def get_cached_products():
#     redis_client = await get_redis()
#     data = await redis_client.get("products_cache")
#
#     return json.loads(data) if data else None
#
#
# async def cache_product(product: ProductResponse):
#     redis_client = await get_redis()
#     await redis_client.set(
#         f"{CACHE_PREFIX}{product.id}", json.dumps(product.model_dump()), ex=CACHE_EXPIRE
#     )
#
#
# async def get_cached_product(product_id: int) -> ProductResponse | None:
#     redis_client = await get_redis()
#     cached_data = await redis_client.get(f"{CACHE_PREFIX}{product_id}")
#     return ProductResponse(**json.loads(cached_data)) if cached_data else None

#------------------------------------------------------------------
async def cache_products(products: list[Product]):
    redis_client = await get_redis()
    # products_data = [product.model_dump() for product in products]
    products_data = [
        ProductResponse.model_validate(product).model_dump(mode="json")
        for product in products
    ]
    await redis_client.set("products_cache", json.dumps(products_data), ex=CACHE_EXPIRE)


async def get_cached_products():
    redis_client = await get_redis()
    data = await redis_client.get("products_cache")

    return json.loads(data) if data else None


async def cache_product(product: ProductResponse):
    redis_client = await get_redis()
    await redis_client.set(
        f"{CACHE_PREFIX}{product.id}",
        json.dumps(product.model_dump()),
        ex=CACHE_EXPIRE
    )

async def get_cached_product(product_id: int) -> ProductResponse | None:
    redis_client = await get_redis()
    cached_data = await redis_client.get(f"{CACHE_PREFIX}{product_id}")
    return ProductResponse(**json.loads(cached_data)) if cached_data else None


# import json
# from typing import Any
#
# import redis.asyncio as redis
#
#
# from app.core.redis import get_redis
# from app.db.models.product import Product
# from app.db.schemas.product import ProductResponse
#
# CACHE_EXPIRE = 600
# # CACHE_PREFIX = "product:"
# PRODUCT_CACHE_PREFIX = "product:"
# PRODUCT_LIST_KEY = "products_cache"
#
#
# async def cache_product(product_id: int, product_data: dict[str, Any]):
#     redis = await get_redis()
#     await redis.set(
#         f"{PRODUCT_CACHE_PREFIX}{product_id}",
#         json.dumps(product_data),
#         ex=CACHE_EXPIRE
#     )
#
#
# async def get_cached_product(product_id: int) -> dict | None:
#     redis = await get_redis()
#     cached_data = await redis.get(f"{PRODUCT_CACHE_PREFIX}{product_id}")
#     return json.loads(cached_data) if cached_data else None
#
#
# async def cache_products_list(products_data: list[dict]):
#     redis = await get_redis()
#     await redis.set(PRODUCT_LIST_KEY, json.dumps(products_data), ex=CACHE_EXPIRE)
#
#
# async def get_cached_products_list() -> list[dict] | None:
#     redis = await get_redis()
#     data = await redis.get(PRODUCT_LIST_KEY)
#     return json.loads(data) if data else None
#
#
# async def invalidate_product_cache(product_id: int):
#     redis = await get_redis()
#     await redis.delete(f"{PRODUCT_CACHE_PREFIX}{product_id}")
#
#
# async def invalidate_products_list_cache():
#     redis = await get_redis()
#     await redis.delete(PRODUCT_LIST_KEY)