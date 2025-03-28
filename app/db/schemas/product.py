from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, condecimal, Field, field_serializer


class ProductUpdate(BaseModel):
    name: None | str = Field(min_length=1, max_length=100)
    description: None | str = Field(None, min_length=10, max_length=1000)
    price: None | condecimal(max_digits=10, decimal_places=2) = None
    category_id: None | int = None

    @field_serializer("price")
    def serialize_price(self, price: condecimal) -> float:
        return float(price)

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=10, max_length=1000)
    price: condecimal(max_digits=10, decimal_places=2)
    # price: float = Field(max_digits=10, decimal_places=2)

    @field_serializer("price")
    def serialize_price(self, price: condecimal) -> float:
        return float(price)


class ProductCreate(ProductBase):
    category_id: int

    class Config:
        from_attributes = True

        @classmethod
        def model_validate(cls, obj: Any):
            return super().model_validate(obj)


class ProductResponse(ProductBase):
    id: int
    category_id: int

    class Config:
        from_attributes = True

