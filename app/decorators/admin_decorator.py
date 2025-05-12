from functools import wraps
from typing import Callable

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.core.security import get_current_user
from app.db.session import get_db
from app.exceptions import ForbiddenException


def requires_admin(role: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user), **kwargs):
            if user.role != role:
                raise ForbiddenException(detail="Insufficient permissions")
            return await func(*args, db=db, user=user, **kwargs)
        return wrapper
    return decorator

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

# def requires_admin(func):
#     @wraps(func)
#     async def wrapper(*args, current_user: UserResponse = Depends(get_admin_user), **kwargs):
#         return await func(*args, current_user=current_user, **kwargs)
#     return wrapper
