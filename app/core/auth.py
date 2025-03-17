# from datetime import datetime, timedelta, timezone
# from typing import TYPE_CHECKING
#
# from fastapi import Depends, HTTPException
# from passlib.context import CryptContext
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from jose import jwt, JWTError
# from starlette import status
#
# from app.core.config import settings
# from app.db.models.user import User
# from app.db.session import get_db
# from app.dependencies import oauth2_scheme
#
# if TYPE_CHECKING:
#     from app.db.repositories.user_repository import UserRepository
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# class AuthService:
#     def __init__(self, user_repo):
#         self.user_repo = user_repo
#
#     async def hash_password(self, password: str) -> str:
#         return pwd_context.hash(password)
#
#     async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
#         return pwd_context.verify(plain_password, hashed_password)
#
#     async def create_access_token(self, data: dict, expires_delta: timedelta = timedelta(hours=1)) -> str:
#         to_encode = data.copy()
#         expire = datetime.now(timezone.utc) + expires_delta
#         to_encode.update({"exp": expire})
#         return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
#
#     async def authenticate_user(self, db: AsyncSession, email: str, password: str):
#         user = await self.user_repo.get_user_by_email(db, email)
#         if not user or not await self.verify_password(password, user.hashed_password):
#             return None
#         return await self.create_access_token({"sub": user.email})
#
# # async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
# #     credentials_exception = HTTPException(
# #         status_code=status.HTTP_401_UNAUTHORIZED,
# #         detail="Could not validate credentials",
# #         headers={"WWW-Authenticate": "Bearer"},
# #     )
# #     # credentials_exception = NotValidCredentialsException()
# #     try:
# #         payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
# #         user_id: str = payload.get("sub")
# #         if not user_id:
# #             raise credentials_exception
# #     except JWTError:
# #         raise credentials_exception
# #
# #     result = await db.execute(select(User).where(User.id == user_id))
# #     user = result.scalars().first()
# #     if not user:
# #         raise credentials_exception
# #     return user

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.repositories.user_repository import UserRepository
from app.db.schemas.user import UserCreate
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    async def authenticate_user(self, email: str, password: str):
        user = await UserRepository.get_user_by_email(self.db, email)
        if not user or not self.verify_password(password, user.hashed_password):
            return False
        return user

    async def register_user(self, user_data: UserCreate):
        hashed_password = self.get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            name=user_data.name,
            surname=user_data.surname,
            phone_number=user_data.phone_number,
            city=user_data.city,
            nova_post_department=user_data.nova_post_department,
            hashed_password=hashed_password
        )
        return await UserRepository.create_user(self.db, user)

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt
