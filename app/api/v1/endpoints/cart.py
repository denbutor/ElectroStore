from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.schemas.cart_item import CartItemResponse, CartItemCreate
from app.db.session import get_db
from app.services.caches.cart_cache import add_to_cart, get_cart
from app.services.cart import CartService

router = APIRouter()

cart_service = CartService()


@router.post("/add", response_model=CartItemResponse)
async def add_item_to_cart(cart_item_data: CartItemCreate, db: AsyncSession = Depends(get_db)):
    await add_to_cart(cart_item_data.user_id, cart_item_data.product_id, cart_item_data.quantity)
    return {"message": "Item added to cart."}

@router.get('/', response_model=dict)
async def get_user_cart(user_id: str):
    return await get_cart(user_id)