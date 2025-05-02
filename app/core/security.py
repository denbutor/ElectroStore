import os
import re
from hashlib import sha256
from typing import Optional
import logging

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User
from starlette import status
from app.core.config import settings
from jose import JWTError, jwt

from app.db.repositories.user_repository import UserRepository
from app.db.schemas.user import UserResponse
from app.db.session import get_db
from passlib.context import CryptContext

from app.dependencies import oauth2_scheme
from app.exceptions import NotValidCredentialsException, ForbiddenException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
   return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
        required_role: Optional[str] = None,
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        print(payload)
        sub = payload.get("sub")
        if not sub:
            raise credentials_exception

        result = await db.execute(select(User).where(User.id == int(sub)))
        user = result.scalars().first()

        print(f"Authenticated user: {user}")  # <-- ДОДАНО

    except (JWTError, ValueError):
        raise credentials_exception

    if not user:
        raise credentials_exception

    if required_role and user.role != required_role:
        raise ForbiddenException(detail="Insufficient permissions")

    return user

    # return UserResponse(id=user.id, email=user.email, role=user.role)


async def get_admin_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
) -> User:
    user = await get_current_user(token, db)

    if user.role != "admin":
        raise ForbiddenException(detail="Only admins can access this resource")

    return user

# async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
#     user = decode_jwt_token(token)  # Декодуємо токен
#
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token",
#         )
#
#     return user
# async def admin_required(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
#     if current_user.role != "admin":
#         raise ForbiddenException()
#     return current_user


# async def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     # token: str,
#     db: AsyncSession = Depends(get_db),
#     required_role: Optional[str] = None,
# ) -> UserResponse:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
#         sub = payload.get("sub")
#         if not sub:
#             raise credentials_exception
#
#         try:
#             user_id = int(sub)
#             result = await db.execute(select(User).where(User.id == user_id))
#         except ValueError:
#             result = await db.execute(select(User).where(User.email == sub))
#
#         user = result.scalars().first()
#     except JWTError:
#         raise credentials_exception
#
#     if not user:
#         raise credentials_exception
#
#     if required_role and user.role != required_role:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Insufficient permissions",
#         )
#
#     # return user
#     return UserResponse(id=user.id, email=user.email)

# def is_valid_jwt(token: str) -> bool:
#     return bool(re.match(r'^[A-Za-z0-9\-_=]+(\.[A-Za-z0-9\-_=]+){2}$', token))
#
# # Функція для отримання користувача
# async def get_current_user(
#     token: str = Depends(oauth2_scheme),  # Ось тут ми використовуємо Depends для отримання токена
#     db: AsyncSession = Depends(get_db),
# ):
#     if not token or not is_valid_jwt(token):  # Перевірка на валідність токена
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid JWT token format",
#         )
#
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
#     try:
#         payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
#         sub = payload.get("sub")
#         if not sub:
#             raise credentials_exception
#
#         try:
#             user_id = int(sub)
#             result = await db.execute(select(User).where(User.id == user_id))
#         except ValueError:
#             result = await db.execute(select(User).where(User.email == sub))
#
#         user = result.scalars().first()
#     except JWTError:
#         raise credentials_exception
#
#     return user

# async def get_current_user(
#         token: str = Depends(oauth2_scheme),
#         db: AsyncSession = Depends(get_db),
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
#     try:
#         payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
#         sub = payload.get("sub")
#         if not sub:
#             raise credentials_exception
#
#         user_repo = UserRepository()
#         user = await user_repo.get_user_by_id(db, int(sub))
#
#         if not user:
#             raise credentials_exception
#
#     except JWTError:
#         raise credentials_exception
#
#     return user