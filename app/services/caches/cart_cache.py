import json

from app.core.redis import get_redis

CART_EXPIRE = 3600

async def add_to_cart(user_id: str, product_id: str, quantity: int):
    redis_client = await get_redis()
    cart_key = f"cart:{user_id}"

    cart = await redis_client.get(cart_key)
    cart = json.loads(cart) if cart else {}

    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    await redis_client.set(cart_key, json.dumps(cart), ex=CART_EXPIRE)

async def get_cart(user_id: str):
    redis_client = await get_redis()
    cart = await redis_client.get(f"cart:{user_id}")
    return json.loads(cart) if cart else {}

async def clear_cart(user_id: str):
    redis_client = await get_redis()
    cart = await redis_client.delete(f"cart:{user_id}")