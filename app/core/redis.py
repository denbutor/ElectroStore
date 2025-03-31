import redis.asyncio as redis
from app.core.config import settings

redis_client = None  # Уникаємо конфлікту назв змінних

async def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = redis.Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True
        )

    return redis_client

# async def get_redis():
#     return redis.Redis.from_url(
#         settings.REDIS_URL,
#         decode_responses=True
#     )

# async def get_redis():
#     global redis_client
#     if redis_client is None:
#         redis_client = redis.Redis.from_url(
#             settings.REDIS_URL,
#             decode_responses=True
#         )
#     try:
#         yield redis_client
#     finally:
#         await redis_client.close()