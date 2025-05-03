from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from typing import List, Dict

# Employee Schema
class EmployeeBase(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    contact_info: Optional[str] = None
    user_id: Optional[int] = None  # Added user_id

class EmployeeCreate(EmployeeBase):
    name: str
    role: str
    user_id: int  # Added user_id

class Employee(EmployeeBase):
    id: int

    class Config:
        orm_mode = True

