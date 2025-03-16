from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class OrderItem(BaseModel):
    product_id: int
    # quantity: int

class OrderBase(BaseModel):
    user_id: int
    items: List[OrderItem]

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True