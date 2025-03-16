from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import product_repository
from app.db.repositories.product_repository import ProductRepository
from app.db.schemas.product import ProductResponse, ProductCreate
from app.db.session import get_db
from app.services.caches.product_cache import get_cached_products, cache_products
from app.services.products import ProductService

router = APIRouter()

product_repo = ProductRepository()

# product_service = ProductService()
#-----------------------------------------------------------------------
#First Version!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#-----------------------------------------------------------------------
# def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
#     return ProductService(product_repo=product_repo)
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
#First GPT Version!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#-----------------------------------------------------------------------
def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(product_repo=product_repo, db=db)
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
#First Version!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#-----------------------------------------------------------------------
# @router.post("/", response_model=ProductResponse)
# async def create_product(
#     product_data: ProductCreate,
#     db: AsyncSession = Depends(get_db),
#     product_service: ProductService = Depends(get_product_service),
# ):
#     product = await product_service.create(db, product_data)
#     await cache_products(await ProductRepository(db).get_products(db))
#     return product
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
#First GPT Version!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#-----------------------------------------------------------------------
@router.post("/", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    product_service: ProductService = Depends(get_product_service),
):
    product = await product_service.create(product_data)
    await cache_products(await product_service.get_products())
    return product
#-----------------------------------------------------------------------


@router.get("/products/")
async def get_products(
    db: AsyncSession = Depends(get_db),
    product_service: ProductService = Depends(get_product_service)
):
    cached = await get_cached_products()
    if cached:
        return cached

    products = await product_service.get_products(db)
    await cache_products(products)
    return products

@router.delete("/products/")
async def delete_product():
    pass

@router.put("/products/")
async def update_product():
    pass