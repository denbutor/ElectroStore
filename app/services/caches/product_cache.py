import json
import redis.asyncio as redis


from app.core.redis import get_redis
from app.db.models.product import Product

CACHE_EXPIRE = 600


async def cache_products(products: list[Product]):
    redis_client = await get_redis()
    products_data = [product.model_dump() for product in products]
    await redis_client.set("products_cache", json.dumps(products_data), ex=CACHE_EXPIRE)


async def get_cached_products():
    redis_client = await get_redis()
    data = await redis_client.get("products_cache")
    return json.loads(data) if data else None
