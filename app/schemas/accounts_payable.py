from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from typing import List, Dict

# Accounts Payable Schema
class AccountsPayableBase(BaseModel):
    vendor_id: Optional[int] = None
    amount: Optional[Decimal] = None
    due_date: Optional[datetime] = None
    status: Optional[bool] = None
    created_at: Optional[datetime] = None
    user_id: Optional[int] = None  # Added user_id

class AccountsPayableCreate(AccountsPayableBase):
    vendor_id: int
    amount: Decimal
    due_date: datetime
    user_id: int  # Added user_id

class AccountsPayable(AccountsPayableBase):
    id: int

    class Config:
        orm_mode = True

