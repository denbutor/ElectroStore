from enum import Enum
# from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.db.base import Base


class UserRole(str, Enum):
    client = "client"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    city = Column(String, nullable=False)
    nova_post_department = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.client, nullable=False)

    orders = relationship("Order", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user")