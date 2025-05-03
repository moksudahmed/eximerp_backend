from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base

class CashFlow(Base):
    __tablename__ = 'cash_flows'
    
    id = Column(Integer, primary_key=True, index=True)
    action_type = Column(String(50), nullable=False)  # e.g., 'CASH_INFLOW', 'CASH_OUTFLOW', 'REGISTER_OPEN', 'REGISTER_CLOSE'
    amount = Column(Numeric(10, 2), nullable=False)  # Cash movement amount
    description = Column(Text, nullable=True)  # Description of the transaction (e.g., payment for product, withdrawal)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Linking to the user who performed the action
    
    # Relationships
 #   user = relationship("User", back_populates="cash_flows")  # CashFlow belongs to User

    # Cash Register-specific fields
    register_balance_before = Column(Numeric(10, 2), nullable=True)  # Balance before the action
    register_balance_after = Column(Numeric(10, 2), nullable=True)  # Balance after the action

    # Optional fields for references (Sale, Expense, etc.)
    related_transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=True)
  #  transaction = relationship("Transaction", back_populates="cash_flows")
