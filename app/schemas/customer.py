from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from typing import List, Dict

# Customer Schema
class CustomerBase(BaseModel):
    name: Optional[str] = None
    contact_info: Optional[str] = None
    user_id: Optional[int] = None  # Added user_id

class CustomerCreate(CustomerBase):
    name: str
    user_id: int  # Added user_id

class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True

