# from uuid import UUID
#
# from pydantic import BaseModel, Field
#
#
# class CartItemBase(BaseModel):
#     product_id: int
#     quantity: int
#
# class CartItemCreate(CartItemBase):
#     user_id: int
#
# class CartItemResponse(CartItemBase):
#     id: int
#     user_id: int
#
#     class Config:
#         from_attributes = True