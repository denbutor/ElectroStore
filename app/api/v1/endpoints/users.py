from fastapi import APIRouter, Depends
from sqlalchemy.testing.pickleable import User

router = APIRouter()
user_service = UserService()

@router.get('/me', response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user_info)):
    return current_user