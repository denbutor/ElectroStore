from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.security import get_current_user
from app.db.schemas.user import UserResponse

router = APIRouter()

@router.get('/dashboard')
async def admin_dashboard(current_user: UserResponse = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Access Denied")
    return {'message': "Admin Dashboard"}