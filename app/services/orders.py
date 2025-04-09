from datetime import datetime

from fastapi import HTTPException
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import redis_client
from app.db.models.order import Order
from app.db.models.order_item import OrderItem
from app.db.models.user import User, UserRole
from app.db.repositories.cart_repository import CartRepository
from app.db.repositories.order_repository import OrderRepository
from app.db.schemas.order import OrderCreate, OrderUpdate, OrderStatus
from app.db.schemas.user import UserResponse


class OrderService:
    def __init__(self, order_repo: OrderRepository, cart_repo: CartRepository, redis_client: Redis = None):
        self.order_repo = order_repo
        self.cart_repo = cart_repo
        self.redis_client = redis_client


    async def get_orders(self, db: AsyncSession, current_user: User):
        if current_user.role == UserRole.admin:
            return await self.order_repo.get_all_orders(db)
        return await self.order_repo.get_user_orders(db, current_user.id)

    async def create_order_from_cart(self, db: AsyncSession, current_user: User):
        # Отримати товари з корзини
        cart_items = await self.cart_repo.get_cart_items(db, current_user.id)
        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        # Обчислити загальну вартість
        total_price = sum(
            item.product.price * item.quantity for item in cart_items
        )

        # Створити замовлення
        new_order = Order(
            user_id=current_user.id,
            total_price=total_price,
            status=OrderStatus.active,
            created_at=datetime.utcnow()

        )
        await db.flush()

        # Створити order_items
        order_items = [
            OrderItem(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=item.product.price
            )
            for item in cart_items
        ]

        # Зберегти замовлення + товари
        order = await self.order_repo.create_order(db, new_order, order_items)

        # Очистити корзину
        await self.cart_repo.clear_cart(db, current_user.id)

        return order

    async def update_order(self, db: AsyncSession, order_id: int, order_data: OrderUpdate, current_user: User):
        order = await self.order_repo.get_order_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if current_user.role != UserRole.admin and order.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this order")

        order.status = order_data.status
        return await self.order_repo.update_order(db, order)

    async def delete_order(self, db: AsyncSession, order_id: int, current_user: UserResponse):
        order = await self.order_repo.get_order_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # if not current_user.is_admin and order.user_id != current_user.id:
        #     raise HTTPException(status_code=403, detail="Not authorized to delete this order")

        await self.order_repo.delete_order(db, order)

        if self.redis_client:
            await self.redis_client.delete(f"order:{order_id}")
            await self.redis_client.delete(f"user:{order.user_id}:orders")

        return {"message": "Order deleted successfully"}


# class OrderService:
#     def __init__(self, order_repo : OrderRepository):
#         self.order_repo  = order_repo
#
#     async def get_orders(self, db: AsyncSession, current_user: User):
#         if current_user.role == UserRole.admin:
#             return await self.order_repo .get_all_orders(db)
#         return await self.order_repo .get_user_orders(db, current_user.id)
#
#     async def create_order(self, db: AsyncSession, user, order_data: OrderCreate):
#
#         new_order = Order(
#             user_id=user.id,
#             total_price=order_data.total_price,
#             status=OrderStatus.active
#         )
#         new_order = await self.order_repo.create_order(db, new_order)
#
#         order_items = [
#             OrderItem(
#                 order_id=new_order.id,
#                 product_id=item.product_id,
#                 quantity=item.quantity,
#                 price_at_purchase=item.price_at_purchase,
#             )
#             for item in order_data.order_items
#         ]
#
#         await self.order_repo.add_order_items(db, order_items)
#
#         return new_order
#
#     async def update_order(self, db: AsyncSession, order_id: int, order_data: OrderUpdate, current_user: User):
#         order = await self.order_repo .get_order_by_id(db, order_id)
#         if not order:
#             raise HTTPException(status_code=404, detail="Order not found")
#         if current_user.role != UserRole.admin and order.user_id != current_user.id:
#             raise HTTPException(status_code=403, detail="Not authorized to update this order")
#
#         order.status = order_data.status
#         return await self.order_repo .update_order(db, order)
#
#     async def delete_order(self, db: AsyncSession, order_id: int, current_user: User):
#         order = await self.order_repo .get_order_by_id(db, order_id)
#         if not order:
#             raise HTTPException(status_code=404, detail="Order not found")
#         if current_user.role != UserRole.admin and order.user_id != current_user.id:
#             raise HTTPException(status_code=403, detail="Not authorized to delete this order")
#
#         await self.order_repo .delete_order(db, order)
#         return {"message": "Order deleted successfully"}
