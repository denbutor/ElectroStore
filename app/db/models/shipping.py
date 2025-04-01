from enum import Enum
from sqlalchemy import Column, String, Integer, ForeignKey,func, Numeric, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base import Base


class ShippingStatus(str, Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"

class ShippingInfo(Base):
    __tablename__ = "shipping_info"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    tracking_number = Column(String(100), unique=True, nullable=True)
    status = Column(SQLEnum(ShippingStatus), default=ShippingStatus.active, nullable=False)
    estimated_delivery = Column(DateTime, nullable=True)

    # order = relationship("Order", back_populates="shipping_info")