from app.core.security import get_current_user
from app.db.models.user import User
from app.db.schemas.cart import CartItemResponse, CartItemCreate, CartResponse
from fastapi import APIRouter, Depends, HTTPException, Body, status, Request
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import CartNotFoundException, CartItemNotFoundException
from app.services.cart import CartService
from app.db.repositories.cart_repository import CartRepository
from app.db.base import get_db
router = APIRouter()
# def get_cart_repository(db: AsyncSession = Depends(get_db)) -> CartRepository:
#     return CartRepository(db)
# def get_cart_service(cart_repo: CartRepository = Depends(get_cart_repository)) -> CartService:
#     return CartService(cart_repo)

cart_repo = CartRepository()
cart_service = CartService(cart_repo)


def get_cart_service() -> CartService:
    return cart_service


@router.get("/", response_model=CartResponse)
async def get_cart(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
        cart_service: CartService = Depends(get_cart_service)
):
    cart = await cart_service.get_cart(current_user.id, db)

    if not cart:
        raise CartNotFoundException()
    return cart


@router.post("/create", response_model=CartResponse)
async def create_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await cart_service.create_cart(current_user.id, db)


@router.post("/add_to_cart", response_model=CartItemResponse)
async def add_to_cart(
    cart_item: CartItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await cart_service.add_to_cart(db, current_user.id, cart_item.product_id, cart_item.quantity)


@router.delete("/remove/{product_id}")
async def remove_from_cart(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await cart_service.remove_from_cart(current_user.id, product_id, db)
    if not success:
        raise CartItemNotFoundException()

@router.delete("/clear")
async def clear_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await cart_service.clear_cart(current_user.id, db)
    if not success:
        raise CartNotFoundException()