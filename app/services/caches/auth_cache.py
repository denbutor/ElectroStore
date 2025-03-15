import redis.asyncio as redis


from app.core.redis import get_redis

TOKEN_EXPIRE = 3600

async def save_token(user_id: str, token: str):
    redis_client = await get_redis()
    await redis_client.set(f"token:{user_id}: token", token, ex=TOKEN_EXPIRE)

async def get_token(user_id: str):
    redis_client = await get_redis()
    return await redis_client.get(f"token:{user_id}: token")

async def revoke_token(user_id: str):
    redis_client = await get_redis()
    return await redis_client.delete(f"token:{user_id}: token")