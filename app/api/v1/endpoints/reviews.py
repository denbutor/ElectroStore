import redis
from fastapi import APIRouter, Depends, HTTPException, Body, status, Request
from redis.asyncio import Redis
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.redis import get_redis
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

# review_repo = ReviewRepository()

# review_service = ReviewService()