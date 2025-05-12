from datetime import datetime

from fastapi import HTTPException
from redis import Redis
from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select

from app.db.models.order import Order
from app.db.models.order_item import OrderItem
from app.db.models.product import Product
from app.db.models.user import User, UserRole
from app.db.repositories.cart_repository import CartRepository
from app.db.repositories.order_repository import OrderRepository
from app.db.schemas.order import OrderStatus

class OrderService:
    def __init__(self, order_repo: OrderRepository, cart_repo: CartRepository, redis_client: Redis = None):
        self.order_repo = order_repo
        self.cart_repo = cart_repo
        self.redis_client = redis_client

    async def search_orders(
            self,
            db: AsyncSession,
            email: str = None,
            product_name: str = None,
            sort_by: str = "created_at",
            sort_order: str = "desc"
    ):
        stmt = (
            select(Order)
            .join(Order.user)
            .join(Order.order_items)
            .join(OrderItem.product)
            .options(
                selectinload(Order.order_items).selectinload(OrderItem.product),
                selectinload(Order.user),
            )
        )

        # Фільтрація
        if email:
            stmt = stmt.where(User.email.ilike(f"%{email}%"))
        if product_name:
            stmt = stmt.where(Product.name.ilike(f"%{product_name}%"))

        # Сортування
        sort_column_map = {
            "created_at": Order.created_at,
            "user_email": User.email,
            "product_name": Product.name,
        }
        column = sort_column_map.get(sort_by, Order.created_at)
        stmt = stmt.order_by(asc(column) if sort_order == "asc" else desc(column))

        result = await db.execute(stmt)
        return result.scalars().unique().all()

    async def create_order_from_cart(self, db, current_user: User) -> Order:
        cart = await self.cart_repo.get_cart_by_user_id(current_user.id, db)
        if not cart or not cart.cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        cart_items = cart.cart_items

        total_price = sum(item.product.price * item.quantity for item in cart_items)

        new_order = Order(
            user_id=current_user.id,
            total_price=total_price,
            status=OrderStatus.active,
            created_at=datetime.utcnow(),
        )
        db.add(new_order)
        await db.flush()

        order_items = [
            OrderItem(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=item.product.price,
            )
            for item in cart_items
        ]

        db.add_all(order_items)
        await db.commit()

        await self.cart_repo.clear_cart(db, current_user.id)

        result = await db.execute(
            select(Order)
            .where(Order.id == new_order.id)
            .options(
                selectinload(Order.order_items).selectinload(OrderItem.product)
            )
        )
        return result.scalars().first()

    async def get_orders(self, db: AsyncSession, current_user: User):
        if current_user.role == UserRole.admin:
            return await self.order_repo.get_all_orders(db)
        return await self.order_repo.get_user_orders(db, current_user.id)

    async def update_order(self, db: AsyncSession, order_id: int, order_data, current_user: User):
        order = await self.order_repo.get_order_by_id(db, order_id)

        if current_user.role != UserRole.admin:
            raise HTTPException(status_code=403, detail="Not authorized to update orders")

        order.status = order_data.status
        return await self.order_repo.update_order(db, order)

    async def delete_order(self, db: AsyncSession, order_id: int, current_user: User):
        order = await self.order_repo.get_order_by_id(db, order_id)

        if current_user.role != UserRole.admin and order.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this order")

        await self.order_repo.delete_order(db, order)

        if self.redis_client:
            await self.redis_client.delete(f"order:{order_id}")
            await self.redis_client.delete(f"user:{order.user_id}:orders")

        return {"message": "Order deleted successfully"}