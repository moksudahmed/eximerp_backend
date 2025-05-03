from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text, Enum
from app.models.enum_types import AccountAction

class JournalEntry(Base):
    __tablename__ = 'journal_entries'

    id = Column(Integer, primary_key=True, index=True)
    narration = Column(String(255), nullable=False)
    debitcredit = Column(Enum(AccountAction, name="accountaction"), nullable=False)    
    amount = Column(Numeric(10, 2), nullable=True)    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)    
    general_ledger_id = Column(Integer, ForeignKey('general_ledger.id'), nullable=False)    
    account_id = Column(Integer, ForeignKey('account.account_id'), nullable=False)
    
    # Relationships
    general_ledger = relationship("GeneralLedger", back_populates="journal_entries")
    account = relationship('Account', back_populates='journal_entries')