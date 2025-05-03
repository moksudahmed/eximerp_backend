from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


# User Model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    sales = relationship("Sale", back_populates="user")
  #  cash_registers = relationship("CashRegister", back_populates="user")    
    transactions = relationship("Transaction", back_populates="user")
    general_ledger = relationship("GeneralLedger", back_populates="user")

    # Use a string for the relationship to resolve the circular dependency
    customers = relationship("Customer", back_populates="user")
    inventory_log = relationship("InventoryLog", back_populates="users")
   # cash_flows = relationship("CashFlow", back_populates="user")    
    
    vendors = relationship("Vendor", back_populates="user")

    accounts_payable = relationship("AccountsPayable", back_populates="users")