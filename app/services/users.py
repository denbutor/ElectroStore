from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.user_repository import UserRepository
from app.db.schemas.user import UserCreate, UserResponse
from app.decorators.auth_decorator import requires_auth
from app.exceptions import NotFoundUserException
from app.services.auth import AuthService

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, db: AsyncSession, user_data: UserCreate, auth_service: AuthService) -> UserResponse:
        """Реєстрація користувача через переданий AuthService"""
        # user_data.password = hashed_password
        hashed_password = await auth_service.hash_password(user_data.password)
        user_dict = user_data.model_dump()
        user_dict["hashed_password"] = hashed_password
        del user_dict["password"]

        new_user = await self.user_repo.create_user(db, user_dict)
        return UserResponse.from_orm(new_user)

    @requires_auth
    async def get_user(self, db: AsyncSession, user_id: str) -> UserResponse:
        user = await self.user_repo.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundUserException()
        return UserResponse.from_orm(user)