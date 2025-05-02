import json
from typing import List

from app.core.redis import get_redis
from app.db.schemas.category import CategoryResponse
from app.db.schemas.product import ProductResponse

CATEGORY_CACHE_KEY = "categories_cache"
CATEGORY_PRODUCTS_CACHE_PREFIX = "category_products_by_name:"
CATEGORY_CACHE_EXPIRE = 60

# Кешування списку категорій
async def cache_categories(categories: List[CategoryResponse]):
    redis = await get_redis()
    data = [category.model_dump(mode="json") for category in categories]
    await redis.set(CATEGORY_CACHE_KEY, json.dumps(data), ex=CATEGORY_CACHE_EXPIRE)

async def get_cached_categories() -> List[CategoryResponse] | None:
    redis = await get_redis()
    raw_data = await redis.get(CATEGORY_CACHE_KEY)
    if not raw_data:
        return None
    parsed = json.loads(raw_data)
    return [CategoryResponse(**item) for item in parsed]

async def cache_category_products_by_name(category_name: str, products: list):
    redis = await get_redis()

    product_schemas = [
        ProductResponse.model_validate(product).model_dump(mode="json")
        for product in products
    ]

    await redis.set(
        f"{CATEGORY_PRODUCTS_CACHE_PREFIX}{category_name}",
        json.dumps(product_schemas),
        ex=CATEGORY_CACHE_EXPIRE
    )

async def get_cached_category_products_by_name(category_name: str) -> list[ProductResponse] | None:
    redis = await get_redis()
    data = await redis.get(f"{CATEGORY_PRODUCTS_CACHE_PREFIX}{category_name}")
    if not data:
        return None

    product_list = json.loads(data)
    return [ProductResponse(**item) for item in product_list]
