from pydantic import BaseModel, ValidationError, ValidationInfo, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
from app.models.enum_types import AccountAction
from typing import List, Optional
# Enum for AccountType

# Enum for AccountType
class AccountTypeEnum(str, Enum):
    ASSET = 'asset'
    LIABILITY = 'liability'
    EQUITY = 'equity'
    REVENUE = 'revenue'
    EXPENSE = 'expense'

# Define JournalEntryCreate as a nested model
class JournalEntryCreate(BaseModel):
    narration: str
    debitcredit: Optional[AccountAction]
    amount: float
    account_id: int

    class Config:
        orm_mode = True


# Define GeneralLedgerCreate as a nested model
class GeneralLedgerCreate(BaseModel):
    ref_no: str
    account_type: AccountTypeEnum
    company: str
    transaction_date: datetime
    user_id: int

    class Config:
        orm_mode = True
  
class CreateLedgerWithEntry(BaseModel):
    general_ledger: GeneralLedgerCreate    
    journal_entries: List[JournalEntryCreate]



class LedgerWithEntryRequest(BaseModel):
    ref_no: str
    account_type: AccountTypeEnum
    company: str
    transaction_date: datetime
    user_id: int
    journal_entries: List[JournalEntryCreate]  # Matches the original JSON key

    class Config:
            orm_mode = True
            
class GeneralLedgerUpdate(BaseModel):
    pass

class JournalEntry(BaseModel):
    narration: Optional[str] 
    debitcredit: Optional[str]   
    amount: Optional[float]    
    created_at: Optional[datetime]
    general_ledger_id: Optional[int]    
    account_id: Optional[int]
    class Config:
        orm_mode = True  # Old config for Pydantic 1.x

class GeneralLedger(BaseModel):
    id: int
    ref_no: Optional[str] = None
    account_type: Optional[AccountTypeEnum]
    company: Optional[str] = None
    transaction_date: datetime = None
    user_id: int
    created_at: datetime
    journal_entries:List[JournalEntry]

    class Config:
        orm_mode = True  # Old config for Pydantic 1.x
