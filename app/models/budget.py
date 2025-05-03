from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base

class Budget(Base):
    __tablename__ = 'budget'
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    budgeted_amount = Column(Numeric(10, 2), nullable=False)
    actual_amount = Column(Numeric(10, 2), nullable=False)
    variance = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="cash_registers")
