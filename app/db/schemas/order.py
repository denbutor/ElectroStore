from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class OrderItem(BaseModel):
    product_id: UUID
    quantity: int

class OrderBase(BaseModel):
    user_id: UUID
    items: List[OrderItem]

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True