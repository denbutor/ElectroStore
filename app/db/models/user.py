# from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum
from sqlalchemy import Column, String, Integer, Enum as SQLEnum
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.db.base import Base

# Base = declarative_base()

class UserRole(str, Enum):
    client = "client"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    # password = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    city = Column(String(100), nullable=False)
    phone_number = Column(String(13), nullable=False)
    nova_post_department = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.client, nullable=False)

    orders = relationship("Order", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user")
