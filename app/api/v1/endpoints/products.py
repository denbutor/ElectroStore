from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.schemas.product import ProductResponse, ProductCreate
from app.db.session import get_db
from app.services.products import ProductService

router = APIRouter()

product_service = ProductService()

@router.get("/", response_model=ProductResponse)
async def create_product(product_data: ProductCreate, db: AsyncSession= Depends(get_db)):
    return await product_service.create_product(db, product_data)