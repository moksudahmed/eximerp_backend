from pydantic import BaseModel
from typing import List

class SaleProductCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    total_price: float
    #itemwise_discount: int

class SaleCreate(BaseModel):
    user_id: int
    total: float
    sale_products: List[SaleProductCreate]
    discount: int

    class Config:
        orm_mode = True
 