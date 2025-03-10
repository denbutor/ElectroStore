from _pytest.nodes import Item
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.cart_item import CartItem
from app.db.repositories.cart_repository import CartRepository
from app.db.schemas.cart_item import CartItemCreate, CartItemResponse


class CartService:
    def __init__(self, cart_repo: CartRepository):
        self.cart_repo = cart_repo

    async def add_to_cart(self, db: AsyncSession, cart_item_data: CartItemCreate) -> CartItemResponse:
        return await self.cart_repo.add_to_cart(db, cart_item_data)

    async def get_cart_items(self, db: AsyncSession, user_id: str):
        return await self.cart_repo.get_cart_items(db, user_id)