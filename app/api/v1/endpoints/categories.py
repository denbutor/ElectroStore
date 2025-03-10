from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.schemas.category import CategoryResponse
from app.db.session import get_db
from app.services.categories import CategoryService

router = APIRouter()

category_service = CategoryService()

@router.get("/", response_model=list[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await category_service.get_categories(db)