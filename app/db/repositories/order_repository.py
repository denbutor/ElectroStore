from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.order import Order
from app.db.repositories.iorder_repository import IOrderRepository


class OrderRepository(IOrderRepository):
    async def create_order(self, db: AsyncSession, order_data: OrderCreate) -> Order:
        new_order = Order(**order_data.dict())
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)
        return new_order