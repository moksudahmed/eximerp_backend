from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from typing import List, Dict

# Vendor Schema
class VendorBase(BaseModel):
    name: Optional[str] = None
    contact_info: Optional[str] = None
    user_id: Optional[int] = None  # Added user_id

class VendorCreate(VendorBase):
    name: str
    user_id: int  # Added user_id

class VendorResponse(BaseModel):
    id: int
    name: Optional[str] = None
    contact_info: Optional[str] = None    

class Vendor(VendorBase):
    id: int
    name: Optional[str] = None
    contact_info: Optional[str] = None   

    class Config:
        orm_mode = True


