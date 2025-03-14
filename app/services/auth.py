from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from app.core.config import settings
from app.db.repositories.user_repository import UserRepository


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def create_access_token(self, data: dict, expires_delta: timedelta = timedelta(hours=1)) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    async def authenticate_user(self, db: AsyncSession, email: str, password: str):
        user = await self.user_repo.get_user_by_email(db, email)
        if not user or not await self.verify_password(password, user.hashed_password):
            return None
        return await self.create_access_token({"sub": user.email})
