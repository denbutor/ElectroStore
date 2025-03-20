from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.order_repository import OrderRepository
from app.db.schemas.order import OrderResponse, OrderCreate
from app.db.session import get_db
from app.services.orders import OrderService

router = APIRouter()

def get_product_service(db: AsyncSession = Depends(get_db)) -> OrderService:
    return OrderService(order_repo=OrderRepository(db))
@router.post("/", response_model=OrderResponse)
async def create_order(
        order_data: OrderCreate,
        # db: AsyncSession= Depends(get_db),
        order_service: OrderService = Depends(get_product_service)
):
    return await order_service.create_order(order_data)

@router.get("/order", response_model=list[OrderResponse])
async def get_user_order(
        user_id: int,
        order_service: OrderService = Depends(get_product_service),
):
    return await order_service.get_orders(user_id)
