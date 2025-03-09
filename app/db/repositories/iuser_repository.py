from abc import abstractmethod, ABC

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, db:AsyncSession, user_data: UserCreate) -> User:
        pass

    @abstractmethod
    async def get_user_by_email(self, db: AsyncSession, email: str) -> User | None:
        pass