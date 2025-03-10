from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.schemas.cart_item import CartItemResponse, CartItemCreate
from app.db.session import get_db
from app.services.cart import CartService

router = APIRouter()

cart_service = CartService()

@router.get('/', response_model=CartItemResponse)
async def add_to_cart(cart_item_data: CartItemCreate, db: AsyncSession = Depends(get_db)):
    return await cart_service.add_to_cart(db, cart_item_data)