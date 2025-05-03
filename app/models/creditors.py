from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base

# CREDITORS MODEL
class Creditor(Base):
    __tablename__ = 'creditors'

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    supplier_name = Column(String(255), nullable=False)
    amount_due = Column(Numeric(10, 2), nullable=False)
    due_date = Column(DateTime, nullable=False)
    status = Column(Boolean, default=False)

    transaction = relationship("Transaction", back_populates="creditors")