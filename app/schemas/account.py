from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional
#from enum_types import AccountTypeEnum
from app.models.enum_types import AccountTypeEnum

class AccountBase(BaseModel):
    #account_id: int
    account_name: str
    account_type: Optional[AccountTypeEnum]
    balance: Optional[Decimal] = None
   #balance: Decimal = Field(..., gt=-0, max_digits=15, decimal_places=2)  # You can also set default values if needed.

    class Config:
        from_attributes = True
        json_encoders = {Decimal: lambda v: str(v)}  # To ensure proper serialization of Decimal types


class AccountCreate(AccountBase):   
    account_name: str
    account_type: Optional[AccountTypeEnum]
    balance: Optional[Decimal] = None

class AccountUpdate(AccountBase):
    pass

class AccountResponse(AccountBase):
    account_id: int   
    account_name: str
    account_type: Optional[AccountTypeEnum]
    balance: Optional[Decimal] = None
    created_at: datetime

    class Config:
        from_attributes = True

class Account(BaseModel):
    account_id: int
    account_name: str
    account_type: Optional[AccountTypeEnum]
    balance: Optional[Decimal] = None
