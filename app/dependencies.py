from app.db.session import get_db


from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_db_dependency():
    async with get_db() as session:
        yield session