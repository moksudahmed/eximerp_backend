from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base

class AccountsPayable(Base):
    __tablename__ = 'accounts_payable'
    id = Column(Integer, primary_key=True, index=True)
    purchase_order_id = Column(Integer, ForeignKey('purchase_orders.id'))    
    amount_due = Column(Numeric(10, 2), nullable=False)
    amount_paid = Column(Numeric(10, 2), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    users = relationship("User", back_populates="accounts_payable")
    purchase_order = relationship("PurchaseOrder", back_populates="accounts_payable")
    
