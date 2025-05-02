from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base


class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    sum_price = Column(Numeric(10, 2), nullable=False, default=0)

    cart = relationship("Cart", back_populates="cart_items")
    # product = relationship("Product")
    product = relationship("Product", back_populates="cart_items")


