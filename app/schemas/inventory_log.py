from pydantic import BaseModel
from enum import Enum
from app.models.enum_types import ActionType
from typing import Optional
from datetime import datetime

class InventoryLogBase(BaseModel):
    product_id: int
    action_type: ActionType
    quantity: int
    user_id: int

class InventoryLogCreate(InventoryLogBase):
    product_id: int
    action_type: ActionType
    quantity: int
    user_id: int
   
class InventoryLogBatchCreate(InventoryLogBase):
    product_id: int
    action_type: ActionType
    quantity: int
    user_id: int
    id:int

    
class InventoryLogUpdate(InventoryLogBase):
    pass

class InventoryLog(InventoryLogBase):
    id: int
    product_id: int
    action_type: ActionType
    quantity: int
    user_id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True