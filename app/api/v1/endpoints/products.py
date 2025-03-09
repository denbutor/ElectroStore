from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

product_service = ProductService()

@router.get("/", response_model=ProductResponse)
async def create_product(product_data: ProductCreate, db: AsyncSession= Depends(get_db)):
    return await product_service.create_product(db, product_data)