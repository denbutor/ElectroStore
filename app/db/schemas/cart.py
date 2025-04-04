from pydantic import BaseModel, conint, condecimal
from typing import List, Optional


class CartItemBase(BaseModel):
    product_id: int
    quantity: conint(ge=1)  # Мінімум 1 товар у кошику
    sum_price: condecimal(max_digits=10, decimal_places=2)  # Два знаки після коми


class CartItemCreate(CartItemBase):
    pass  # Використовується при додаванні товару в кошик


class CartItemResponse(CartItemBase):
    id: int

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
