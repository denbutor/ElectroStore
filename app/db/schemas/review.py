from pydantic import BaseModel, Field
from datetime import datetime


class ReviewBase(BaseModel):
    product_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(ReviewBase):
    pass


class ReviewOut(ReviewBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes  = True

