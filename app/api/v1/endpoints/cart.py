from app.core.security import get_current_user
from app.db.models.user import User
from app.db.schemas.cart import CartItemResponse, CartItemCreate, CartResponse
from fastapi import APIRouter, Depends, HTTPException, Body, status, Request
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
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


@router.get("/cart", response_model=CartResponse)
async def get_cart(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
        cart_service: CartService = Depends(get_cart_service)
):
    cart = await cart_service.get_cart(current_user.id, db)

    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

    return cart


@router.post("/cart/create", response_model=CartResponse)
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


@router.delete("/cart/remove/{product_id}")
async def remove_from_cart(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await cart_service.remove_from_cart(current_user.id, product_id, db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")


@router.delete("/cart/clear")
async def clear_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await cart_service.clear_cart(current_user.id, db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")


# @router.get("/cart/{user_id}", response_model=CartResponse)
# async def get_cart(user_id: int, db: AsyncSession = Depends(get_db)):
#     cart = await cart_service.get_cart(user_id, db)
#     if not cart:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
#     return cart
#
# @router.post("/cart/{user_id}/create", response_model=CartResponse)
# async def create_cart(user_id: int, db: AsyncSession = Depends(get_db)):
#     cart = await cart_service.create_cart(user_id, db)
#     return cart
#
# # @router.post("/cart/{user_id}/add", response_model=CartItemCreate)
# # async def add_to_cart(user_id: int, cart_item: CartItemCreate, db: AsyncSession = Depends(get_db)):
# #     cart_item = await cart_service.add_to_cart(user_id, cart_item.product_id, cart_item.quantity, db)
# #     return cart_item
#
# @router.post("/add_to_cart")
# async def add_to_cart(
#         user_id: int,
#         cart_item: CartItemCreate,
#         db: AsyncSession = Depends(get_db),
#         cart_service: CartService = Depends(get_cart_service)
# ):
#     cart_item_response = await cart_service.add_to_cart(db, user_id, cart_item.product_id, cart_item.quantity)
#
#     # Перетворюємо об'єкт CartItem на CartItemResponse
#     # cart_item_response = CartItemResponse.model_validate(cart_item_obj)
#
#     return cart_item_response
#
#
# @router.delete("/cart/{user_id}/remove/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def remove_from_cart(user_id: int, product_id: int, db: AsyncSession = Depends(get_db)):
#     success = await cart_service.remove_from_cart(user_id, product_id, db)
#     if not success:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
#     return
#
# @router.delete("/cart/{user_id}/clear", status_code=status.HTTP_204_NO_CONTENT)
# async def clear_cart(user_id: int, db: AsyncSession = Depends(get_db)):
#     success = await cart_service.clear_cart(user_id, db)
#     if not success:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
#     return
