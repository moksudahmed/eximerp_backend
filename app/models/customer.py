from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base


# Customer Model
class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contact_info = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Establish the back_populates from the User side
    user = relationship("User", back_populates="customers")
    sales = relationship("Sale", back_populates="customers")

