from uuid import UUID

from pydantic import BaseModel, condecimal


class ProductBase(BaseModel):
    name: str
    description: str
    price: condecimal(max_digits=10, decimal_places=2)

class ProductCreate(ProductBase):
    category_id: UUID

class ProductUpdate(ProductBase):
    id: UUID
    category_id: UUID

    class Config:
        from_attributes = True