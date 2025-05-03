from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base

# Enum for register actions
class CashActionType(enum.Enum):
    OPEN = 'OPEN'
    CLOSE = 'CLOSE'
    CASH_INFLOW = 'CASH_INFLOW'
    CASH_OUTFLOW = 'CASH_OUTFLOW'

# Cash Register model
class CashRegister(Base):
    __tablename__ = 'cash_registers'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action_type = Column(Enum(CashActionType, name="cash_action_enum"), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

  #  user = relationship("User", back_populates="cash_registers")
