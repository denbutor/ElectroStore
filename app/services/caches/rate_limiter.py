from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.redis import get_redis
from app.exceptions import TooManyRequestsException

LIMIT = 10
WINDOW = 60

class RateLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        redis = await get_redis()
        ip = request.client.host
        key = f"rate_limit: {ip}:{request.url.path}"


        requests = await redis.get(key)
        if requests and int(requests) >= LIMIT:
            # raise HTTPException(status_code=429, detail="Too many requests")
            raise TooManyRequestsException()

        await redis.incr(key)
        await redis.expire(key, WINDOW)

        response = await call_next(request)
        return response
