from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.schemas.order import OrderResponse, OrderCreate
from app.db.session import get_db
from app.services.orders import OrderService

router = APIRouter()

order_service = OrderService()

@router.get("/", response_model=OrderResponse)
async def create_order(order_data: OrderCreate, db: AsyncSession= Depends(get_db)):
    return await order_service.create_order(db, order_data)