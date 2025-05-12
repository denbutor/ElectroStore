import redis
from fastapi import APIRouter, Depends, HTTPException, Body, status, Request
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.redis import get_redis
# from app.core.auth import AuthService
from app.core.security import get_current_user, get_admin_user
from app.db.base import async_engine, AsyncSessionLocal
from app.db.models.product import Product
from app.db.models.user import User

from app.db.repositories import product_repository
from app.db.repositories.product_repository import ProductRepository
from app.db.schemas.product import ProductResponse, ProductCreate, ProductUpdate
from app.db.schemas.user import UserResponse
from app.db.session import get_db
from app.decorators.admin_decorator import requires_admin
from app.exceptions import ForbiddenException, ProductNotFoundException
from app.services.caches.product_cache import get_cached_products, cache_products, cache_product
from app.services.products import ProductService

router = APIRouter()

product_repo = ProductRepository()


async def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    redis_client = await get_redis()
    product_repo = ProductRepository()
    return ProductService(product_repo=product_repo, redis_client=redis_client)

@router.post("/create", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_db),
    product_service: ProductService = Depends(get_product_service),
    current_user: UserResponse = Depends(get_admin_user),
    ):
    product_service = ProductService(product_repo, redis)
    return await product_service.create_product(db, product_data)

@router.put("/update/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
    # admin_user: Depends(get_admin_user),
    product_service: ProductService = Depends(get_product_service),
    current_user: UserResponse = Depends(get_admin_user),
):
    product_service = ProductService(product_repo, redis)
    updated_product = await product_service.update_product(db, product_id, product_data)
    if not updated_product:
        raise ProductNotFoundException()
    return updated_product
    # return await product_service.update_product(db, product_id, updated_data)

@router.delete("/delete/{product_id}")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis),
    product_service: ProductService = Depends(get_product_service),
    current_user: UserResponse = Depends(get_admin_user),
):
    deleted = await product_service.delete_product(db, product_id)
    if not deleted:
        raise ProductNotFoundException()


@router.get("/", response_model=list[ProductResponse])
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

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_by_id(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    product_service: ProductService = Depends(get_product_service)
):
    product = await product_service.get_product_by_id(db, product_id)
    if not product:
        raise ProductNotFoundException()
    # await cache_product(product)
    return product

@router.get("/search/{name}", response_model=list[ProductResponse])
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


