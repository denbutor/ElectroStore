from abc import abstractmethod, ABC
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.order import Order
from app.db.models.order_item import OrderItem
from app.db.schemas.order import OrderCreate


class IOrderRepository(ABC):
    @abstractmethod
    async def get_all_orders(self, db: AsyncSession):
        pass

    @abstractmethod
    async def get_user_orders(self, db: AsyncSession, user_id: int):
        pass

    @abstractmethod
    async def get_order_by_id(self, db: AsyncSession, order_id: int):
        pass

    @abstractmethod
    async def update_order(self, db: AsyncSession, order: Order):
        pass

    @abstractmethod
    async def create_order(self, db: AsyncSession, order: Order, order_items: list[OrderItem]) -> Order:
        pass

    @abstractmethod
    async def delete_order(self, db: AsyncSession, order: Order):
        pass
