# from abc import abstractmethod, ABC
#
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.db.models.cart_item import CartItem
# from app.db.schemas.cart_item import CartItemCreate
#
#
# class ICartRepository(ABC):
#     @abstractmethod
#     async def add_to_cart(self, db: AsyncSession, cart_item_data: CartItemCreate) -> CartItem:
#         pass