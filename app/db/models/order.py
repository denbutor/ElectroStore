from enum import Enum
from sqlalchemy import Column, String, Integer, ForeignKey,func, Numeric, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base import Base
# from app.db.models.user import User


class OrderStatus(str, Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.active, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    user = relationship("User", back_populates='orders')
    # order_items = relationship("OrderItem", back_populates="order", cascade="all, delete")
    # shipping_info = relationship("ShippingInfo", back_populates="order", uselist=False, cascade="all, delete")
