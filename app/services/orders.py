from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.order_repository import OrderRepository
from app.db.schemas.order import OrderCreate, OrderResponse
from app.decorators.admin_decorator import requires_admin


class OrderService:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    async def create_order(self, db: AsyncSession, order_data: OrderCreate) -> OrderResponse:
        return await self.order_repo.create_order(db, order_data)

    @requires_admin
    async def get_orders(self, db: AsyncSession, user_id: str):
        return await self.order_repo.get_orders(db, user_id)