from sqlalchemy import Column, Integer, ForeignKey, Float, Numeric, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    status = Column(Integer, default="active", nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    user = relationship('User', back_populates='orders')
