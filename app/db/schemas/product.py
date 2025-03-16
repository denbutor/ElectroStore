from uuid import UUID

from pydantic import BaseModel, condecimal, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=10, max_length=1000)
    price: condecimal(max_digits=10, decimal_places=2)

class ProductCreate(ProductBase):
    category_id: int

class ProductResponse(ProductBase):
    id: int
    category_id: int

    class Config:
        from_attributes = True