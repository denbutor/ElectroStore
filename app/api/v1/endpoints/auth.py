# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.core.security import get_current_user
# from app.db.models.user import User
# from app.db.repositories.user_repository import UserRepository
# from app.exceptions import NotAuthException
# from app.core.auth import AuthService
# from app.services.users import UserService
# from app.db.schemas.user import UserCreate, UserResponse, AuthResponse
# from app.dependencies import get_db
# from app.services.caches.auth_cache import save_token, revoke_token
#
# router = APIRouter(prefix="/auth", tags=["auth"])
#
# user_repo = UserRepository()
# # auth_service = AuthService()
# def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
#     return AuthService(user_repo=user_repo)
#
# user_service = UserService(user_repo)
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
# @router.post("/register", response_model=AuthResponse)
# async def register(
#         user_data: UserCreate,
#         db: AsyncSession = Depends(get_db),
#         auth_service: AuthService = Depends(get_auth_service)
# ):
#     user = await user_service.create_user(db, user_data, auth_service)
#     token = await auth_service.create_access_token({"sub": user.email})
#     await save_token(user.id, token)
#
#     return AuthResponse(
#         access_token=token,
#         token_type="bearer",
#         user=UserResponse.model_validate(user)
#     )
#
# @router.post("/login", response_model=AuthResponse)
# async def login(
#         user_data: UserCreate,
#         db: AsyncSession = Depends(get_db),
#         auth_service: AuthService = Depends(get_auth_service)
# ):
#     user = await user_repo.get_user_by_email(db, user_data.email)
#     if not user or not await auth_service.verify_password(user_data.password, user.hashed_password):
#         raise NotAuthException()
#
#     token = await auth_service.create_access_token({"sub": user.email})
#     await save_token(user.id, token)
#     return AuthResponse(
#         access_token=token,
#         token_type="bearer",
#         user=UserResponse.model_validate(user)
#     )
#
# @router.get("/logout")
# async def logout(user_id: str):
#     await revoke_token(user_id)
#     return {"message": "Successfully logged out"}
#
#
# @router.post("/auth/token", response_model=AuthResponse)
# async def login(
#         form_data: OAuth2PasswordRequestForm = Depends(),
#         db: AsyncSession = Depends(get_db)
# ):
#     # user_repo = UserRepository(db)
#     auth_service = AuthService(user_repo)
#
#     user = await user_repo.get_user_by_email(db, form_data.username)
#     if not user or not await auth_service.verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Incorrect email or password")
#
#     token = await auth_service.create_access_token({"sub": str(user.id)})
#
#     return AuthResponse(
#         access_token=token,
#         token_type="bearer",
#         user=UserResponse(id=user.id, email=user.email)
#     )
#
#
# @router.get("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.db.repositories.user_repository import UserRepository
from app.db.schemas.user import UserCreate, UserResponse, AuthResponse
from app.core.auth import AuthService
from app.db.session import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    existing_user = await UserRepository.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await auth_service.register_user(user_data)
    return user

@router.post("/login", response_model=AuthResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": user}

@router.post("/token", response_model=AuthResponse)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": user}
