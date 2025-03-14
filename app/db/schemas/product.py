from uuid import UUID

from pydantic import BaseModel, condecimal


class ProductBase(BaseModel):
    name: str
    description: str
    price: condecimal(max_digits=10, decimal_places=2)

class ProductCreate(ProductBase):
    category_id: int

class ProductResponse(ProductBase):
    id: int
    category_id: int

    class Config:
        from_attributes = True