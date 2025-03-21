from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.cart_repository import CartRepository
from app.db.schemas.cart_item import CartItemResponse, CartItemCreate
from app.db.session import get_db
from app.services.caches.cart_cache import add_to_cart, get_cart
from app.services.cart import CartService

router = APIRouter()

# cart_service = CartService()
def get_cart_service(db: AsyncSession = Depends(get_db)) -> CartService:
    return CartService(cart_repo=CartRepository(db))

@router.post("/add", response_model=CartItemResponse)
async def add_item_to_cart(
        cart_item_data: CartItemCreate,
        db: AsyncSession = Depends(get_db),
        cart_service: CartService = Depends(get_cart_service),
):
    cart_item = await cart_service.add_to_cart(cart_item_data)
    await add_to_cart(cart_item_data.user_id, cart_item_data.product_id, cart_item_data.quantity)
    return cart_item, {"message": "Item added to cart."}

@router.get('/', response_model=dict)
async def get_user_cart(
        user_id: int,
        cart_service: CartService = Depends(get_cart_service),
):
    cart_items = await cart_service.get_cart_items(user_id)
    return cart_items