from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.schemas.user import UserResponse
from app.services.users import UserService
from app.db.session import get_db
from app.db.repositories.user_repository import UserRepository

router = APIRouter()

@router.get('/me', response_model=UserResponse)
async def get_current_user(
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(user_repo=UserRepository())
    return await user_service.get_user(db=db, user_id=current_user.id)
