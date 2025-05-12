
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
        # to_encode.update({"exp": expire})
        to_encode.update({"exp": expire, "sub": str(data["sub"]), "role": data.get("role", "user")})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt