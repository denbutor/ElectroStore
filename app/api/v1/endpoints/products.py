from fastapi import APIRouter, Depends, HTTPException, Body, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

# from app.core.auth import AuthService
from app.core.security import get_current_user, get_admin_user
from app.db.models.user import User

from app.db.repositories import product_repository
from app.db.repositories.product_repository import ProductRepository
from app.db.schemas.product import ProductResponse, ProductCreate, ProductUpdate
from app.db.schemas.user import UserResponse
from app.db.session import get_db
from app.decorators.admin_decorator import requires_admin
from app.exceptions import ForbiddenException, ProductNotFoundException
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
    return ProductService(product_repo=product_repo)
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
# @requires_admin
async def create_product(
    product_data: ProductCreate,
    # current_user: User,
    db: AsyncSession = Depends(get_db),
    product_service: ProductService = Depends(get_product_service),
    current_user: UserResponse = Depends(get_admin_user),
    ):

    # if current_user.role != "admin":
    #     raise ForbiddenException()


    # if get_current_user(required_role="admin"):
    #     raise ForbiddenException()

    # product = await product_service.create_product(db, product_data)
    # products = await product_service.get_products(db)
    #
    # await cache_products(products)
    # return product
    return await product_service.create_product(db, product_data)

#-----------------------------------------------------------------------


@router.get("/products/", response_model=list[ProductResponse])
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

@router.get("/products/{name}", response_model=ProductResponse)
async def get_product_by_name(
    name: str,
    db: AsyncSession = Depends(get_db),
    product_service: ProductService = Depends(get_product_service)
):
    product = await product_service.get_product_by_name(db, name)
    if not product:
        raise ProductNotFoundException()
    await cache_products(product)
    return product

@router.get("/products/search/{name}", response_model=list[ProductResponse])
async def search_products_by_name(
    name: str,
    db: AsyncSession = Depends(get_db),
    product_service: ProductService = Depends(get_product_service)
):
    product = await product_service.search_products_by_name(db, name)
    if not product:
        raise ProductNotFoundException()
    await cache_products(product)
    return product

@router.put("/products/{product_id}", response_model=ProductResponse)
@requires_admin
async def update_product(
    product_id: int,
    updated_data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    product_service: ProductService = Depends(get_product_service)
):
    # try:
    #     print(updated_data.model_dump())
    #     return await product_service.update_product(db, product_id, updated_data)
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=str(e))
    return await product_service.update_product(db, product_id, updated_data)



@router.delete("/products/{product_id}")
@requires_admin
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    product_service: ProductService = Depends(get_product_service)
):
    # try:
    #     await product_service.delete_product(db, product_id)
    #     return {"message": "Product deleted successfully"}
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=str(e))
    await product_service.delete_product(db, product_id)
    return {"message": "Product deleted successfully"}



# @router.post("/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
# def create_product(
#         product: ProductCreate,
#         db: Session = Depends(get_db),
#         current_user=Depends(AuthService.admin_required)
# ):
#     return ProductRepository.create_product(db, product)
#
#
# @router.get("/products/{product_id}", response_model=ProductResponse)
# def get_product(product_id: int, db: Session = Depends(get_db)):
#     product = ProductRepository.get_product_by_id(db, product_id)
#     if not product:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
#     return product
#
#
# @router.put("/products/{product_id}", response_model=ProductResponse)
# def update_product(
#         product_id: int,
#         product_data: ProductUpdate,
#         db: Session = Depends(get_db),
#         current_user=Depends(AuthService.admin_required)
# ):
#     updated_product = ProductRepository.update_product(db, product_id, product_data)
#     if not updated_product:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
#
#     return updated_product
#
#
# @router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_product(
#         product_id: int,
#         db: Session = Depends(get_db),
#         current_user=Depends(AuthService.admin_required)
# ):
#     deleted = ProductRepository.delete_product(db, product_id)
#     if not deleted:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
