from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    title: Optional[str] = None
    unit_price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None

class ProductCreate(ProductBase):
    title: str
    unit_price: float
    stock: int
    category:str
    sub_category:str
    
class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True