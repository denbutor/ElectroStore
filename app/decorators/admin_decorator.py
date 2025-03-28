from functools import wraps
from typing import Callable

from fastapi import Depends, Request, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.schemas.user import UserResponse
from app.core.security import get_current_user, get_admin_user
from app.db.session import get_db
from app.dependencies import oauth2_scheme
from app.exceptions import ForbiddenException

# def requires_admin(func):
#     @wraps(func)
#     async def wrapper(*args, current_user: UserResponse = None, **kwargs):
#         if current_user is None:
#             current_user = await get_current_user()
#
#         if current_user.role != 'admin':
#             raise ForbiddenException()
#
#         return await func(*args, **kwargs)
#
#     return wrapper

# def requires_admin(func):
#     @wraps(func)
#     async def wrapper(*args, **kwargs):
#         current_user = kwargs.get("current_user")  # Отримуємо користувача з аргументів
#         if not current_user or current_user.role != "admin":
#             raise ForbiddenException()
#         return await func(*args, **kwargs)
#     return wrapper

# def requires_admin(func):
#     @wraps(func)
#     async def wrapper(*args, **kwargs):
#         current_user = None
#
#         # Шукаємо current_user серед аргументів
#         for arg in args:
#             if isinstance(arg, UserResponse):
#                 current_user = arg
#                 break
#
#         if not current_user or current_user.role != "admin":
#             raise ForbiddenException(detail="Insufficient permissions")
#
#         return await func(*args, **kwargs)
#
#     return wrapper

def requires_admin(func):
    @wraps(func)
    async def wrapper(*args, current_user: UserResponse = Depends(get_admin_user), **kwargs):
        return await func(*args, current_user=current_user, **kwargs)
    return wrapper
