from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.order import Order
from app.db.models.order_item import OrderItem
from app.db.models.user import User, UserRole
from app.db.repositories.order_repository import OrderRepository
from app.db.schemas.order import OrderCreate, OrderUpdate, OrderStatus


class OrderService:
    def __init__(self, order_repo : OrderRepository):
        self.order_repo  = order_repo

    async def get_orders(self, db: AsyncSession, current_user: User):
        if current_user.role == UserRole.admin:
            return await self.order_repo .get_all_orders(db)
        return await self.order_repo .get_user_orders(db, current_user.id)

    async def create_order(self, db: AsyncSession, user, order_data: OrderCreate):
        """Логіка створення замовлення"""

        # 1️⃣ Створюємо замовлення
        new_order = Order(
            user_id=user.id,
            total_price=order_data.total_price,
            status=OrderStatus.active
        )
        new_order = await self.order_repo.create_order(db, new_order)

        # 2️⃣ Створюємо список товарів у замовленні
        order_items = [
            OrderItem(
                order_id=new_order.id,  # ✅ order_id тепер є!
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=item.price_at_purchase,
            )
            for item in order_data.order_items
        ]

        # 3️⃣ Зберігаємо товари та завершуємо транзакцію
        await self.order_repo.add_order_items(db, order_items)

        return new_order

    async def update_order(self, db: AsyncSession, order_id: int, order_data: OrderUpdate, current_user: User):
        order = await self.order_repo .get_order_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if current_user.role != UserRole.admin and order.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this order")

        order.status = order_data.status
        return await self.order_repo .update_order(db, order)

    async def delete_order(self, db: AsyncSession, order_id: int, current_user: User):
        order = await self.order_repo .get_order_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if current_user.role != UserRole.admin and order.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this order")

        await self.order_repo .delete_order(db, order)
        return {"message": "Order deleted successfully"}
