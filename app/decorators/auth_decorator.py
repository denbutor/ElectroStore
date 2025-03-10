from fastapi import HTTPException, status,Depends
from app.db.schemas.user import UserResponse
from app.core.security import get_current_user


def requires_auth():
    async def auth_dependency(current_user: UserResponse = Depends(get_current_user)):
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        return current_user
    return auth_dependency