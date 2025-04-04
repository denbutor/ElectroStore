from pydantic import BaseModel, condecimal
from typing import List
from enum import Enum
from datetime import datetime

class OrderStatus(str, Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    price_at_purchase: condecimal(max_digits=10, decimal_places=2)

class OrderItemResponse(OrderItemBase):
    id: int
    price_at_purchase: condecimal(max_digits=10, decimal_places=2)

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    status: OrderStatus = OrderStatus.active

class OrderCreate(OrderBase):
    total_price: condecimal(max_digits=10, decimal_places=2)
    items: List[OrderItemCreate]

class OrderUpdate(OrderBase):
    status: OrderStatus

class OrderResponse(OrderBase):
    id: int
    user_id: int
    total_price: condecimal(max_digits=10, decimal_places=2)
    created_at: datetime
    order_items: List[OrderItemResponse]

    class Config:
        from_attributes = True
