from sqlalchemy import Column, Integer, Float, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base

# SaleProduct Model
class SaleProduct(Base):
    __tablename__ = 'sale_products'

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey('sales.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Float, nullable=False)
   
    sale = relationship("Sale", back_populates="sale_products")
    product = relationship("Product", back_populates="sale_products")
