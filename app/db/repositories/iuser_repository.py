from abc import abstractmethod, ABC

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.schemas.user import UserCreate


class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, db: AsyncSession, user: User) -> User:
        pass

    @abstractmethod
    async def get_user_by_id(self, db: AsyncSession, user_id: int):
        pass

    # @abstractmethod
    # async def get_user_by_id(self, db: AsyncSession, user_id: int) -> User | None:
    #     pass

    @abstractmethod
    async def get_user_by_email(self, db: AsyncSession, email: str) -> User | None:
        pass

    @abstractmethod
    async def update_user(self, db: AsyncSession, user_id: int, user_data: dict) -> User:
        pass
