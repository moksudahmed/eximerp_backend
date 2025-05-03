from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base

class AccountsReceivable(Base):
    __tablename__ = 'accounts_receivable'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    invoice_id = Column(Integer, ForeignKey('invoices.id'))
    amount = Column(Numeric(10, 2), nullable=False)
    due_date = Column(DateTime, nullable=False)
    status = Column(Boolean, default=False)  # Paid or Unpaid
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="cash_registers")


