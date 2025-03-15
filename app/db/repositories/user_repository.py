from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User
from app.db.repositories.iuser_repository import IUserRepository
from typing import Optional
from app.db.schemas.user import UserCreate
from app.core.security import hash_password
from app.factories.user_factory import UserFactory
from app.services.auth import AuthService


class UserRepository(IUserRepository):

    async def create_user(self, db: AsyncSession, user_data: UserCreate, auth_service: AuthService) -> User:
        hashed_password = await auth_service.hash_password(user_data.password)
        user_data_dict = user_data.model_dump()
        user_data_dict["hashed_password"] = hashed_password
        del user_data_dict["password"]

        new_user = User(**user_data_dict)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    async def get_user_by_id(self, db: AsyncSession, user_id: str) ->  User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, db: AsyncSession, email: str) ->  User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

