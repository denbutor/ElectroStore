from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.models.order import Order
from app.db.models.order_item import OrderItem
from app.db.repositories.iorder_repository import IOrderRepository

class OrderRepository(IOrderRepository):
    async def get_all_orders(self, db: AsyncSession):
        result = await db.execute(select(Order).options(selectinload(Order.order_items)))
        return result.scalars().all()

    async def create_order(
        self,
        db: AsyncSession,
        order: Order,
        order_items: list[OrderItem]
    ) -> Order:
        db.add(order)
        await db.flush()  # Щоб отримати order.id

        if not order_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        for item in order_items:
            item.order_id = order.id
            db.add(item)

        await db.commit()
        await db.refresh(order)
        return order

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
        order = result.scalars().first()
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
        # return result.scalars().first()

    # async def create_order(self, db: AsyncSession, order: Order, order_items: list[OrderItem]):
    #     db.add(order)
    #     await db.flush()
    #
    #     for item in order_items:
    #         db.add(item)
    #
    #     await db.commit()
    #     await db.refresh(order)
    #     return order

    # async def update_order(self, db: AsyncSession, order: Order):
    #     db.add(order)
    #     await db.commit()
    #     await db.refresh(order)
    #     return order

    async def update_order(self, db: AsyncSession, order: Order):
        existing_order = await db.execute(select(Order).where(Order.id == order.id))
        existing_order = existing_order.scalars().first()
        if not existing_order:
            raise HTTPException(status_code=404, detail="Order not found")
        existing_order.status = order.status  # приклад оновлення статусу
        await db.commit()
        await db.refresh(existing_order)
        return existing_order


    async def delete_order(self, db: AsyncSession, order: Order):
        await db.delete(order)
        await db.commit()

# class OrderRepository(IOrderRepository):
#     async def get_all_orders(self, db: AsyncSession):
#         result = await db.execute(
#             select(Order).options(selectinload(Order.order_items))
#         )
#         return result.scalars().all()
#
#     async def get_user_orders(self, db: AsyncSession, user_id: int):
#         result = await db.execute(
#             select(Order)
#             .where(Order.user_id == user_id)
#             .options(selectinload(Order.order_items))
#         )
#         return result.scalars().all()
#
#     async def get_order_by_id(self, db: AsyncSession, order_id: int):
#         result = await db.execute(
#             select(Order)
#             .where(Order.id == order_id)
#             .options(selectinload(Order.order_items))
#         )
#         return result.scalars().first()
#
#     async def create_order(self, db: AsyncSession, order: Order, order_items: list[OrderItem]):
#         db.add(order)
#         for item in order_items:
#             db.add(item)
#         await db.commit()
#         await db.refresh(order)
#         return order
#
#     async def update_order(self, db: AsyncSession, order: Order):
#         db.add(order)
#         await db.commit()
#         await db.refresh(order)
#         return order
#
#     async def delete_order(self, db: AsyncSession, order: Order):
#         await db.delete(order)
#         await db.commit()
