from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

class CashActionTypeEnum(str, Enum):
    OPEN = 'OPEN'
    CLOSE = 'CLOSE'
    CASH_INFLOW = 'CASH_INFLOW'
    CASH_OUTFLOW = 'CASH_OUTFLOW'


class CashFlowBase(BaseModel):
    user_id: int
    action_type: CashActionTypeEnum
    amount: float
    description: Optional[str] = None  # Allow description to be None
    register_balance_before: float
    register_balance_after: float

class OpenRegisterRequest(BaseModel):
    user_id: int
    amount: float
    description: Optional[str] = None

class CloseRegisterRequest(BaseModel):
    user_id: int       
    description: Optional[str] = None 

class CashFlowCreate(CashFlowBase):
    user_id: int
    action_type: CashActionTypeEnum
    amount: float
    description: str = None
    register_balance_before: float
    register_balance_after: float
    # created_at: str

class CashFlowUpdate(CashFlowBase):
    pass

class CashFlow(CashFlowBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
