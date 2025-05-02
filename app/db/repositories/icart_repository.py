from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.cart import Cart
from app.db.models.cart_item import CartItem



class ICartRepository(ABC):
    @abstractmethod
    async def create_cart(self, user_id: int, db: AsyncSession) -> Cart:
        pass

    @abstractmethod
    async def add_to_cart(self, db: AsyncSession, user_id: int, product_id: int, quantity: int) -> CartItem:
        pass

    @abstractmethod
    async def remove_from_cart(self, db: AsyncSession, user_id: int, product_id: int) -> bool:
        pass

    @abstractmethod
    async def clear_cart(self, db: AsyncSession, user_id: int) -> bool:
        pass

    @abstractmethod
    async def get_cart_by_user_id(self, user_id: int, db: AsyncSession) -> Cart | None:
        pass

    # @abstractmethod
    # async def get_cart_items(self, db: AsyncSession, user_id: int) -> list[CartItem]:
    #     pass

    # @abstractmethod
    # async def get_cart_items(self, user_id: int, db: AsyncSession):
    #     pass

