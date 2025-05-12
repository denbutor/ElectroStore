from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User
from app.db.repositories.user_repository import UserRepository
from app.db.schemas.user import UserCreate, UserResponse, UserUpdate
from app.exceptions import NotFoundUserException
from app.core.auth import AuthService

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, db: AsyncSession, user_data: UserCreate, auth_service: AuthService) -> UserResponse:
        hashed_password = await auth_service.hash_password(user_data.password)
        user_data_dict = user_data.model_dump()
        user_data_dict["hashed_password"] = hashed_password

        new_user = await self.user_repo.create_user(db, UserCreate(**user_data_dict), auth_service)
        return UserResponse.model_validate(new_user)

    # @requires_auth
    async def get_user(self, db: AsyncSession, user_id: int) -> UserResponse:
        user = await self.user_repo.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundUserException()
        return UserResponse.model_validate(user)

    async def get_users_by_email(self, db: AsyncSession, email: str) -> User:
        return await self.user_repo.get_user_by_email(db, email)

    async def get_all_users(self, db: AsyncSession):
        return await self.user_repo.get_all_users(db)

    async def update_user(self, db: AsyncSession, user_id: int, user_update: UserUpdate):
        return await self.user_repo.update_user(db, user_id, user_update)

    async def delete_user(self, db: AsyncSession, user_id: int):
        return await self.user_repo.delete_user(db, user_id)

