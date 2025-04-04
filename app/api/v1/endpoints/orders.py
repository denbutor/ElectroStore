from app.db.models.user import User
from app.db.repositories.order_repository import OrderRepository
from app.db.schemas.order import OrderResponse, OrderCreate, OrderUpdate
from app.db.session import get_db
from app.services.orders import OrderService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.security import get_current_user
router = APIRouter()

# router = APIRouter(prefix="/orders", tags=["Orders"])

order_service = OrderService(OrderRepository())

def get_order_service() -> OrderService:
    return OrderService(OrderRepository())

@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = OrderService(OrderRepository())
    return await service.get_orders(db, current_user)

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = OrderService(OrderRepository())
    return await service.create_order(db, order_data, current_user)

@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = OrderService(OrderRepository())
    return await service.update_order(db, order_id, order_data, current_user)

@router.delete("/{order_id}", status_code=status.HTTP_200_OK)
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = OrderService(OrderRepository())
    return await service.delete_order(db, order_id, current_user)
