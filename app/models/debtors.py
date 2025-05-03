from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base


# DEBTORS MODEL
class Debtor(Base):
    __tablename__ = 'debtors'

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    customer_name = Column(String(255), nullable=False)
    amount_owed = Column(Numeric(10, 2), nullable=False)
    due_date = Column(DateTime, nullable=False)
    status = Column(Boolean, default=False)

    transaction = relationship("Transaction", back_populates="debtors")
