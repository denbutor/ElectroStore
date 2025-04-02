from enum import Enum
from sqlalchemy import Column, String, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.models.review import Review
from app.db.models.cart import Cart

class UserRole(str, Enum):
    client = "client"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    hashed_password = Column(String, nullable=False)

    city = Column(String(100), nullable=False)
    phone_number = Column(String(13), nullable=False)
    nova_post_department = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.client, nullable=False)

    cart = relationship("Cart", back_populates="user", cascade="all, delete", uselist=True)
    orders = relationship("Order", back_populates="user", cascade="all, delete")
    reviews = relationship("Review", back_populates="user", cascade="all, delete")
