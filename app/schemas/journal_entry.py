from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class JournalEntryBase(BaseModel):
    narration: Optional[str]
    debitcredit: Optional[str]   
    amount: Optional[float]    
    created_at: Optional[datetime]
    general_ledger_id: Optional[int]    
    account_id: Optional[int]

class JournalEntryCreate(BaseModel):
    narration: str
    debitcredit: str
    amount: float
    general_ledger_id: int
    account_id: int


class JournalEntryUpdate(BaseModel):
    narration: Optional[str] = None
    debitcredit: Optional[str] = None  
    amount: Optional[float] = None    
    

class JournalEntry(JournalEntryBase):
    id: int
    general_ledger_id: int
    account_id: int

    class Config:
       from_attributes = True