from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.cart_repository import CartRepository
from app.db.schemas.cart import CartResponse, CartItemResponse

class CartService:
    def __init__(self, cart_repo: CartRepository):
        self.cart_repo = cart_repo

    async def get_cart(self, user_id: int, db: AsyncSession) -> CartResponse | None:
        cart = await self.cart_repo.get_cart_by_user_id(user_id, db)
        if not cart:
            return None
        return CartResponse.model_validate(cart)

    async def create_cart(self, user_id: int, db: AsyncSession) -> CartResponse:
        cart = await self.cart_repo.create_cart(user_id, db)
        return CartResponse(id=cart.id, user_id=cart.user_id, cart_items=[])

    async def add_to_cart(self, db: AsyncSession, user_id: int, product_id: int, quantity: int) -> CartItemResponse:
        cart_item = await self.cart_repo.add_to_cart(db, user_id, product_id, quantity)
        return CartItemResponse.model_validate(cart_item)

    async def remove_from_cart(self, user_id: int, product_id: int, db: AsyncSession) -> bool:
        return await self.cart_repo.remove_from_cart(db, user_id, product_id)

    async def clear_cart(self, user_id: int, db: AsyncSession) -> bool:
        return await self.cart_repo.clear_cart(db, user_id)