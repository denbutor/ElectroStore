from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.services.auth import AuthService
from app.db.schemas.user import UserCreate, UserResponse
from app.dependencies import get_db
from app.services.caches.auth_cache import save_token, revoke_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    user = await auth_service.register(user_data)
    token = auth_service.create_access_token(user)
    await save_token(user.id, token)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=UserResponse)
async def login(user_data: UserResponse, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    user = await auth_service.authenticate(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = auth_service.create_access_token(user)
    await save_token(user.id, token)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/logout")
async def logout(user_id: str):
    await revoke_token(user_id)
    return {"message": "Successfully logged out"}