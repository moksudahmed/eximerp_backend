from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from typing import List, Dict


# Payroll Schema
class PayrollBase(BaseModel):
    employee_id: Optional[int] = None
    salary: Optional[Decimal] = None
    tax: Optional[Decimal] = None
    net_pay: Optional[Decimal] = None
    payment_date: Optional[datetime] = None
    user_id: Optional[int] = None  # Added user_id

class PayrollCreate(PayrollBase):
    employee_id: int
    salary: Decimal
    tax: Decimal
    net_pay: Decimal
    payment_date: datetime
    user_id: int  # Added user_id


class Payroll(PayrollBase):
    id: int

    class Config:
        orm_mode = True

