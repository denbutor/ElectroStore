from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.order import Order


class IOrderRepository(ABC):
    @abstractmethod
    async def create_order(self, db: AsyncSession, order_data: OrderCreate) -> Order:
        pass