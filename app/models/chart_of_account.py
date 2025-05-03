from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text, Enum as SqlEnum
from enum import Enum
from app.models.enum_types import AccountTypeEnum

class ChartOfAccount(Base):
    __tablename__ = "chart_of_accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_name = Column(String(255), nullable=False)
    account_type = Column(Enum(AccountTypeEnum), nullable=False)
    parent_account_id = Column(Integer, ForeignKey("chart_of_accounts.id"), nullable=True)

    # Optional parent-child relationship for hierarchical accounts
    parent_account = relationship("ChartOfAccount", remote_side=[id], backref="sub_accounts")

    # Relation with General Ledger and Journal Entries
    general_ledger_entries = relationship("GeneralLedger", back_populates="chart_of_account")
    journal_entries = relationship("JournalEntry", back_populates="chart_of_account")

