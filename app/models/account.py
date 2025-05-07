from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text, Enum as SqlEnum
#from enum_types import AccountTypeEnum
from app.models.enum_types import AccountTypeEnum
import datetime

class Account(Base):
    __tablename__ = 'account'
    
    account_id = Column(Integer, primary_key=True)    
    account_name = Column(String, nullable=False, unique=True)  # Unique constraint added
    account_type = Column(Enum(AccountTypeEnum, name="accounttypeenum"), nullable=False)  # e.g., Asset, Liability, Equity
    balance = Column(Numeric(15, 2), nullable=False)  
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    transactions = relationship('Transaction', back_populates='account')
    journal_entries = relationship('JournalEntry', back_populates='account')
    
  #  general_ledgers = relationship('GeneralLedger', back_populates='account')