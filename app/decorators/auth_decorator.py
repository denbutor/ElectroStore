from fastapi import Depends
from functools import wraps
from app.db.schemas.user import UserResponse
from app.core.security import get_current_user
from app.exceptions import NotAuthException

def requires_auth(func):
    @wraps(func)
    async def wrapper(*args, current_user: UserResponse = Depends(get_current_user), **kwargs):
        if not current_user:
            raise NotAuthException

        return await func(*args, **kwargs)

    return wrapper