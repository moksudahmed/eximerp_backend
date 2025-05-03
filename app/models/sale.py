from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


# Sale Model
class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, index=True)    
    total = Column(Float, nullable=False)
    discount = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="sales")
    sale_products = relationship("SaleProduct", back_populates="sale")
    # Use a string for the relationship to resolve the circular dependency
    customers = relationship("Customer", back_populates="sales")
