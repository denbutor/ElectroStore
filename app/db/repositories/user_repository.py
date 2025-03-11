from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User
from app.db.repositories.iuser_repository import IUserRepository
from app.db.schemas.user import UserCreate
from app.core.security import hash_password
from app.factories.user_factory import UserFactory


class UserRepository(IUserRepository):
    async def create_user(self, db: AsyncSession, user_data: UserCreate) -> User:
        hashed_password = hash_password(user_data.password)
        new_user = UserFactory(**user_data.dict(), password=hashed_password)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    async def get_user_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
