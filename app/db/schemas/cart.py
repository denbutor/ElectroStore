from pydantic import BaseModel, conint, condecimal
from typing import List, Optional

from app.db.schemas.product import ProductResponse


class CartItemBase(BaseModel):
    quantity: conint(ge=1)  # Мінімум 1 товар у кошику
    sum_price: condecimal(max_digits=10, decimal_places=2)  # Два знаки після коми
    product: ProductResponse


class CartItemCreate(CartItemBase):
    product_id: int

    class Config:
        from_attributes = True


class CartItemResponse(CartItemBase):
    id: int
    product_id: int


    class Config:
        from_attributes = True  # Працює з ORM (SQLAlchemy)


class CartBase(BaseModel):
    user_id: int

    class Config:
        from_attributes = True


class CartResponse(CartBase):
    id: int
    cart_items: List[CartItemResponse] = []  # Список товарів у кошику

    class Config:
        from_attributes = True
