from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.user_repository import UserRepository
from app.db.schemas.user import UserCreate, UserResponse
from app.decorators.auth_decorator import requires_auth


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, db: AsyncSession, user_data: UserCreate) -> UserResponse:
        return await self.user_repo.create_user(db, user_data)

    @requires_auth
    async def get_user(self, db: AsyncSession, user_data: UserCreate) -> UserResponse:
        return await self.user_repo.get_user(db, user_data)