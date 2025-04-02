from enum import Enum
from sqlalchemy import Column, String, Integer, ForeignKey,func, Numeric, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base import Base
# from app.db.models.user import User
# from app.db.models.cart_item import CartItem

class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates='cart')
    cart_items = relationship("CartItem", back_populates="cart", cascade="all, delete")
