from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.db.schemas.user import UserResponse
from app.services.users import UserService

router = APIRouter()
user_service = UserService()

@router.get('/me', response_model=UserResponse)
async def get_current_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user