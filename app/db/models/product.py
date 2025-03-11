from sqlalchemy import Column, String, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base


class Product(Base):
     __tablename__ = 'products'

     id = Column(Integer, index=True, primary_key=True)
     category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
     name = Column(String(100), nullable=False)
     description = Column(String(1000), nullable=False)
     price = Column(Numeric(10, 2), nullable=False)

     category = relationship('Category', back_populates='products')