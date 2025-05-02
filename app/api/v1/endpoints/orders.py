from redis import Redis

from app.core.redis import get_redis
from app.db.models.user import User
from app.db.repositories.cart_repository import CartRepository
from app.db.repositories.order_repository import OrderRepository
from app.db.schemas.order import OrderResponse, OrderCreate, OrderUpdate
from app.db.schemas.user import UserResponse
from app.db.session import get_db
from app.services.orders import OrderService
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.security import get_current_user, get_admin_user

router = APIRouter()

# router = APIRouter(prefix="/orders", tags=["Orders"])

# order_service = OrderService(OrderRepository())
order_service = OrderService(OrderRepository(), CartRepository())


# def get_order_service() -> OrderService:
#     return OrderService(OrderRepository())

def get_order_service() -> OrderService:
    return OrderService(OrderRepository(), CartRepository())

@router.get("/search", response_model=List[OrderResponse])
async def search_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_admin_user),  # 🔐 тільки для адмінів
    email: str = Query(None),
    product_name: str = Query(None),
    sort_by: str = Query("created_at"),  # або "user_email", "product_name"
    sort_order: str = Query("desc"),     # або "asc"
):
    return await order_service.search_orders(
        db, email=email, product_name=product_name,
        sort_by=sort_by, sort_order=sort_order
    )

@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await order_service.get_orders(db, current_user)

@router.post("/from-cart", response_model=OrderResponse)
async def create_order_from_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return await order_service.create_order_from_cart(db, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{order_id}", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    order_data: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await order_service.update_order(db, order_id, order_data, current_user)

@router.delete("/{order_id}", status_code=status.HTTP_200_OK)
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await order_service.delete_order(db, order_id, current_user)

# @router.get("/", response_model=List[OrderResponse])
# async def get_orders(
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user),
#     # current_user: UserResponse = Depends(get_admin_user),
# ):
#     # service = OrderService(OrderRepository())
#     service = OrderService(OrderRepository(), CartRepository())
#     return await service.get_orders(db, current_user)
#
# # @router.post("/from-cart", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
# # async def create_order_from_cart(
# #     db: AsyncSession = Depends(get_db),
# #     current_user: User = Depends(get_current_user)
# # ):
# #     service = OrderService(OrderRepository(), CartRepository())
# #     return await service.create_order_from_cart(db, current_user)
#
# # @router.post("/from-cart", response_model=OrderResponse)
# # async def create_order_from_cart(
# #     db: AsyncSession = Depends(get_db),
# #     current_user: User = Depends(get_current_user)
# # ):
# #     service = OrderService(OrderRepository(), CartRepository())
# #
# #     try:
# #         order = await service.create_order_from_cart(db, current_user)
# #     except ValueError as e:
# #         raise HTTPException(status_code=400, detail=str(e))
# #     print(f"Creating order for user: {current_user.id}")
# #
# #     return order
#
# @router.post("/from-cart", response_model=OrderResponse)
# async def create_order_from_cart(
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     service = OrderService(OrderRepository(), CartRepository())
#
#     try:
#         created_order = await service.create_order_from_cart(db, current_user)
#         full_order = await service.get_full_order(db, created_order.id)  # ✅ окреме завантаження order_items + product
#         return full_order
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
# # @router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
# # async def create_order(
# #     order_data: OrderCreate,
# #     db: AsyncSession = Depends(get_db),
# #     current_user: User = Depends(get_current_user)
# # ):
# #     # service = OrderService(OrderRepository())
# #     service = OrderService(OrderRepository(), CartRepository())
# #     return await service.create_order(db, order_data, current_user)
#
# @router.put("/{order_id}", response_model=OrderResponse)
# async def update_order(
#     order_id: int,
#     order_data: OrderUpdate,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     # service = OrderService(OrderRepository())
#     service = OrderService(OrderRepository(), CartRepository())
#     return await service.update_order(db, order_id, order_data, current_user)
#
# # @router.delete("/{order_id}", status_code=status.HTTP_200_OK)
# # async def delete_order(
# #     order_id: int,
# #     db: AsyncSession = Depends(get_db),
# #     current_user: UserResponse = Depends(get_admin_user)
# # ):
# #     # service = OrderService(OrderRepository())
# #     service = OrderService(OrderRepository(), CartRepository())
# #     return await service.delete_order(db, order_id, current_user)
#
# @router.delete("/{order_id}", status_code=status.HTTP_200_OK)
# async def delete_order(
#     order_id: int,
#     db: AsyncSession = Depends(get_db),
#     redis_client: Redis = Depends(get_redis),
#     # current_user: UserResponse = Depends(get_current_user),
#     current_user: UserResponse = Depends(get_admin_user)
# ):
#     service = OrderService(OrderRepository(), CartRepository(), redis_client)
#     return await service.delete_order(db, order_id, current_user)

