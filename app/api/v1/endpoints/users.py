from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import AuthService
from app.core.security import get_current_user, get_admin_user
from app.db.models.user import User

from app.db.schemas.user import UserResponse, UserUpdate
from app.exceptions import NotFoundUserException
from app.services.users import UserService
from app.db.session import get_db
from app.db.repositories.user_repository import UserRepository

router = APIRouter()

user_service = UserService(UserRepository())

@router.get("/me", response_model=UserResponse)
async def get_my_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_my_info(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    updated_user = await user_service.update_user(db, current_user.id, user_update)
    if not updated_user:
        raise NotFoundUserException()
    return updated_user



@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_account(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = await user_service.delete_user(db, current_user.id)
    if not deleted:
        raise NotFoundUserException()

@router.get("/admin/users", response_model=list[UserResponse])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    # admin_user: User = Depends(get_admin_user),
    current_user: UserResponse = Depends(get_admin_user),
):
    users = await user_service.get_all_users(db)
    return users

@router.get("/admin/user/{email}", response_model=UserResponse)
async def get_users_by_email(
    email: str = None,
    db: AsyncSession = Depends(get_db),
    # admin_user: User = Depends(get_admin_user),
    current_user: UserResponse = Depends(get_admin_user),
):
    users = await user_service.get_users_by_email(db, email)
    return users

@router.put("/admin/users/{user_id}", response_model=UserResponse)
async def update_user_by_admin(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    # admin_user: User = Depends(get_admin_user),
    current_user: UserResponse = Depends(get_admin_user),
):
    updated_user = await user_service.update_user(db, user_id, user_update)
    if not updated_user:
        raise NotFoundUserException()
    return updated_user

@router.delete("/admin/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_admin(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    # admin_user: User = Depends(get_admin_user),
    current_user: UserResponse = Depends(get_admin_user),
):
    deleted = await user_service.delete_user(db, user_id)
    if not deleted:
        raise NotFoundUserException()