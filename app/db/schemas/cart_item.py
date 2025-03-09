from uuid import UUID

from pydantic import BaseModel


class CartItemBase(BaseModel):
    product_id: UUID
    quantity: int

class CartItemCreate(CartItemBase):
    user_id: UUID

class CartItemResponse(CartItemBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True