from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base

class Payroll(Base):
    __tablename__ = 'payroll'
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    salary = Column(Numeric(10, 2), nullable=False)
    tax = Column(Numeric(10, 2), nullable=False)
    net_pay = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="cash_registers")
