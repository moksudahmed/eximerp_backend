from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from typing import List, Dict

# Budget Schema
class BudgetBase(BaseModel):
    account_id: Optional[int] = None
    budgeted_amount: Optional[Decimal] = None
    actual_amount: Optional[Decimal] = None
    variance: Optional[Decimal] = None
    created_at: Optional[datetime] = None
    user_id: Optional[int] = None  # Added user_id

class BudgetCreate(BudgetBase):
    account_id: int
    budgeted_amount: Decimal
    actual_amount: Decimal
    variance: Decimal
    user_id: int  # Added user_id

class Budget(BudgetBase):
    id: int

    class Config:
        orm_mode = True
