from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

# Product Model
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    unit_price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(String(255), nullable=False, index=True)
    sub_category = Column(String(255), nullable=False, index=True)

    sale_products = relationship("SaleProduct", back_populates="product")
    inventory_log = relationship("InventoryLog", back_populates="product")