from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.db.repositories.user_repository import UserRepository
from app.db.schemas.user import UserCreate, UserResponse, AuthResponse
from app.core.auth import AuthService
from app.db.session import get_db
from app.exceptions import EmailExistException, IncorrectLoginException

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=200)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    existing_user = await UserRepository.get_user_by_email(db, user_data.email)
    if existing_user:
        raise EmailExistException()
        # raise HTTPException(status_code=400, detail="Email already registered")

    user = await auth_service.register_user(user_data)
    return user

@router.post("/login", response_model=AuthResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise IncorrectLoginException()

    # access_token = auth_service.create_access_token(data={"sub": user.email})
    access_token = auth_service.create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer", "user": user}

@router.post("/token", response_model=AuthResponse)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        # raise IncorrectLoginException()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # access_token = auth_service.create_access_token(data={"sub": user.email})
    access_token = auth_service.create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer", "user": user}
