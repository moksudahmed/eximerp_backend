from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from typing import List, Dict


# Accounts Receivable Schema
class AccountsReceivableBase(BaseModel):
    customer_id: Optional[int] = None
    invoice_id: Optional[int] = None
    amount: Optional[Decimal] = None
    due_date: Optional[datetime] = None
    status: Optional[bool] = None
    user_id: Optional[int] = None  # Added user_id

class AccountsReceivableCreate(AccountsReceivableBase):
    customer_id: int
    invoice_id: int
    amount: Decimal
    due_date: datetime
    user_id: int  # Added user_id

class AccountsReceivable(AccountsReceivableBase):
    id: int

    class Config:
        orm_mode = True

