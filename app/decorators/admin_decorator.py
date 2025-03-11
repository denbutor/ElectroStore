from fastapi import HTTPException, status
from fastapi.params import Depends

from app.core.security import get_current_user
from app.db.schemas.user import UserResponse


def requires_admin():
    async def admin_dependency(current_user: UserResponse = Depends(get_current_user)):
        if current_user.role != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not an admin')
        return current_user
    return admin_dependency