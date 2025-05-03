from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from typing import List, Dict


# Financial Report Schema
class FinancialReportBase(BaseModel):
    report_type: Optional[str] = None
    generated_at: Optional[datetime] = None
    data: Optional[Dict] = None  # Store report data as a flexible JSON object
    user_id: Optional[int] = None  # Added user_id


class FinancialReportCreate(FinancialReportBase):
    report_type: str
    data: Dict
    user_id: int  # Added user_id

class FinancialReport(FinancialReportBase):
    id: int

    class Config:
        orm_mode = True

