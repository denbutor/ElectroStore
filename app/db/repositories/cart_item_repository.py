from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.cart_item import CartItem
from app.db.repositories.icart_item_repository import ICartRepository
from app.db.schemas.cart_item import CartItemCreate


class CartRepository(ICartRepository):
    async def add_to_cart(self, db: AsyncSession, cart_item_data: CartItemCreate) -> CartItem:
        new_cart_item = CartItem(**cart_item_data.dict())
        db.add(new_cart_item)
        await db.commit()
        await db.refresh(new_cart_item)
        return new_cart_item