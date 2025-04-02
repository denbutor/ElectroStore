from sqlalchemy import Column, String, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.models.order_item import OrderItem


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product", cascade="all, delete")
    order_items = relationship("OrderItem", back_populates="product", cascade="all, delete")
    reviews = relationship("Review", back_populates="product", cascade="all, delete")
