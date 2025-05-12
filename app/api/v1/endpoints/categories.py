from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas.category import CategoryResponse
from app.db.schemas.product import ProductResponse
from app.db.session import get_db
from app.db.repositories.category_repository import CategoryRepository
from app.services.categories import CategoryService

router = APIRouter()

category_repo=CategoryRepository()

def get_category_service(db: AsyncSession = Depends(get_db)) -> CategoryService:
    return CategoryService(category_repo=category_repo)

@router.get("/", response_model=list[CategoryResponse])
async def get_categories(
    db: AsyncSession = Depends(get_db),
    category_service: CategoryService = Depends(get_category_service),
):
    return await category_service.get_categories(db)

@router.get("/name/{category_name}/products", response_model=list[ProductResponse])
async def get_products_in_category_by_name(
    category_name: str,
    db: AsyncSession = Depends(get_db),
    category_service: CategoryService = Depends(get_category_service),
):
    return await category_service.get_category_products_by_name(db, category_name)

