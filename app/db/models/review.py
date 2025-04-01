from sqlalchemy import Column, Integer, ForeignKey, Float, Numeric,String, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(1000), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")