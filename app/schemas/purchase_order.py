from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from decimal import Decimal
from enum import Enum
from app.models.enum_types import OrderStatusEnum

class VendorBase(BaseModel):
    name: str
    contact_info: Optional[str] = None

class VendorResponse(VendorBase):
    id: int

    class Config:
        orm_mode = True
        

class PurchaseOrderItemBase(BaseModel):
   # purchase_order_id: Optional[int]
    product_id: Optional[int]
    quantity: Optional[int]
    cost_per_unit: Optional[Decimal]
    class Config:
        orm_mode = True

class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    pass

class PurchaseOrderItemResponse(PurchaseOrderItemBase):
    #id: int
   # purchase_order_id: Optional[int]
    product_id: Optional[int]
    quantity: Optional[int]
    cost_per_unit: Optional[Decimal]

    class Config:
        orm_mode = True

class PurchaseOrderBase(BaseModel):
    #id: Optional[int]
    vendor_id: Optional[int] 
    date: Optional[date]
    total_amount: Optional[Decimal]
    status: Optional[OrderStatusEnum]
    user_id: Optional[int]

    class Config:
        orm_mode = True

class PurchaseOrderCreate(PurchaseOrderBase):  
    vendor_id: Optional[int]
    date: Optional[date]
    total_amount: Optional[Decimal]
    status: Optional[OrderStatusEnum]
    user_id: Optional[int]
    items: List[PurchaseOrderItemBase]

    class Config:
        orm_mode = True

class PurchaseOrderResponse(PurchaseOrderBase):
    id: int
    vendor_id: int
    date: date
    total_amount: Decimal
    status: OrderStatusEnum
    items: List[PurchaseOrderItemResponse]

    class Config:
        orm_mode = True

class PurchaseOrderItem(BaseModel):
    product_id: int
    quantity: int
    cost_per_unit: Decimal

    class Config:
        orm_mode = True

class PurchaseOrder(BaseModel):
    id: int
    vendor_id: int
    date: date
    total_amount: Decimal
    status: OrderStatusEnum
    items: List[PurchaseOrderItem]
    user_id: int
    class Config:
        orm_mode = True
