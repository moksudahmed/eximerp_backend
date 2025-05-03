from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.db.base import Base

class OrderStatus(PyEnum):
    PENDING = "PENDING"
    RECEIVED = "RECEIVED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_info = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    # Relationships
    user = relationship("User", back_populates="vendors")
    purchase_orders = relationship("PurchaseOrder", back_populates="vendor")
