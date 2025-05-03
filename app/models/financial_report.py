from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base
from sqlalchemy.dialects.postgresql import JSON

class FinancialReport(Base):
    __tablename__ = 'financial_reports'
    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String(255), nullable=False)  # e.g. Balance Sheet, Profit and Loss
    generated_at = Column(DateTime, server_default=func.now(), nullable=False)
    data = Column(JSON, nullable=False)  # Store report data as JSON for flexibility
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="cash_registers")
