from fastapi import HTTPException, status
from fastapi.params import Depends
from app.core.security import get_current_user
from app.db.schemas.user import UserResponse
from fastapi import HTTPException, status, Depends
from functools import wraps
from app.db.schemas.user import UserResponse
from app.core.security import get_current_user
from app.exceptions import NotAuthException, ForbiddenException


def requires_admin(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        current_user: UserResponse = await get_current_user()
        if current_user.role != 'admin':
            raise ForbiddenException

        return await func(*args, **kwargs)

    return wrapper