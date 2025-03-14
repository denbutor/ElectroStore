from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas.category import CategoryResponse
from app.db.session import get_db
from app.db.repositories.category_repository import CategoryRepository
from app.services.categories import CategoryService

router = APIRouter()

# Функція для створення CategoryService
def get_category_service(db: AsyncSession = Depends(get_db)) -> CategoryService:
    return CategoryService(category_repo=CategoryRepository(db))

@router.get("/", response_model=list[CategoryResponse])
async def get_categories(
    db: AsyncSession = Depends(get_db),
    category_service: CategoryService = Depends(get_category_service),  # Отримуємо сервіс через Depends
):
    return await category_service.get_categories(db)
