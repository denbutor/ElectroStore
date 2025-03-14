from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.user_repository import UserRepository
from app.exceptions import NotAuthException
from app.services.auth import AuthService
from app.services.users import UserService
from app.db.schemas.user import UserCreate, UserResponse, AuthResponse
from app.dependencies import get_db
from app.services.caches.auth_cache import save_token, revoke_token

router = APIRouter(prefix="/auth", tags=["auth"])

user_repo = UserRepository()
# auth_service = AuthService()
def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(user_repo=UserResponse)
user_service = UserService(user_repo)


@router.post("/register", response_model=AuthResponse)
async def register(
        user_data: UserCreate,
        db: AsyncSession = Depends(get_db),
        auth_service: AuthService = Depends(get_auth_service)
):
    user = await user_service.create_user(db, user_data, auth_service)  # Передаємо auth_service в метод
    token = await auth_service.create_access_token({"sub": user.email})
    await save_token(user.id, token)

    # Повертаємо і користувача, і токен
    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user=user  # Повертаємо інформацію про користувача
    )

@router.post("/login", response_model=UserResponse)
async def login(
        user_data: UserCreate,
        db: AsyncSession = Depends(get_db),
        auth_service: AuthService = Depends(get_auth_service)
):
    user = await user_repo.get_user_by_email(db, user_data.email)
    if not user or not await auth_service.verify_password(user_data.password, user.hashed_password):
        raise NotAuthException()

    token = await auth_service.create_access_token({"sub": user.email})
    await save_token(user.id, token)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/logout")
async def logout(user_id: str):
    await revoke_token(user_id)
    return {"message": "Successfully logged out"}
