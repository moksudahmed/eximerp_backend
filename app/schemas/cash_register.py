from pydantic import BaseModel
from enum import Enum
from typing import Optional

class CashActionTypeEnum(str, Enum):
    OPEN = 'OPEN'
    CLOSE = 'CLOSE'
    CASH_INFLOW = 'CASH_INFLOW'
    CASH_OUTFLOW = 'CASH_OUTFLOW'

class CashRegisterBase(BaseModel):
    user_id: int
    action_type: CashActionTypeEnum
    amount: float
    description: str = None

class CashRegisterCreate(CashRegisterBase):
    user_id: int
    action_type: CashActionTypeEnum
    amount: float
    description: str = None
    # created_at: str

class CashRegisterUpdate(CashRegisterBase):
    pass

class CashRegister(CashRegisterBase):
    id: int

    class Config:
        orm_mode = True
