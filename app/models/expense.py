from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base

# EXPENSE MODEL
class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    category = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    expense_date = Column(DateTime, server_default=func.now(), nullable=False)

    transaction = relationship("Transaction", back_populates="expense")