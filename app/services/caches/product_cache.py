import json
import redis.asyncio as redis


from app.core.redis import get_redis
from app.db.models.product import Product
from app.db.schemas.product import ProductResponse

CACHE_EXPIRE = 30
CACHE_PREFIX = "product:"

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