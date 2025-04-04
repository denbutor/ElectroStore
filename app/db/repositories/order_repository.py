from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.models.order import Order
from app.db.models.order_item import OrderItem
from app.db.repositories.iorder_repository import IOrderRepository


class OrderRepository(IOrderRepository):
    async def get_all_orders(self, db: AsyncSession):
        result = await db.execute(
            select(Order).options(selectinload(Order.order_items))
        )
        return result.scalars().all()

    async def get_user_orders(self, db: AsyncSession, user_id: int):
        result = await db.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.order_items))
        )
        return result.scalars().all()

    async def get_order_by_id(self, db: AsyncSession, order_id: int):
        result = await db.execute(
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.order_items))
        )
        return result.scalars().first()

    async def create_order(self, db: AsyncSession, order: Order, order_items: list[OrderItem]):
        db.add(order)
        for item in order_items:
            db.add(item)
        await db.commit()
        await db.refresh(order)
        return order

    async def update_order(self, db: AsyncSession, order: Order):
        db.add(order)
        await db.commit()
        await db.refresh(order)
        return order

    async def delete_order(self, db: AsyncSession, order: Order):
        await db.delete(order)
        await db.commit()
