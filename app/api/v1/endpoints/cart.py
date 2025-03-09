from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

cart_service = CartService()

@router.get('/', response_model=CartItemResponse)
async def add_to_cart(cart_item_data: CartItemCreate, db: AsyncSession = Depends(get_db)):
    return await cart_service.add_to_cart(db, cart_item_data)