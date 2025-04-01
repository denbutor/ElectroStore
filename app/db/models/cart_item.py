from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base


# class CartItem(Base):
#     __tablename__ = 'cart_items'
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#     product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
#     quantity = Column(Integer, nullable=False)
#
#     user = relationship('User', back_populates='cart_items')
#     product = relationship('Product')

class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    sum_price = Column(Numeric(10, 2), nullable=False)

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product")