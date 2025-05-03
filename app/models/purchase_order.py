from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from enum import Enum
import enum
from datetime import date
from app.models.enum_types import OrderStatusEnum
from app.db.base import Base
from sqlalchemy.dialects.postgresql import ENUM as PgEnum


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"    
    id = Column(Integer, primary_key=True, autoincrement=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False, default=date.today)
    total_amount = Column(Float, nullable=False)    
    status = Column(PgEnum(OrderStatusEnum, name='order_status'), nullable=False, default=OrderStatusEnum.PENDING)    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    vendor = relationship("Vendor", back_populates="purchase_orders")
    items = relationship("PurchaseOrderItem", back_populates="purchase_order")    
    accounts_payable = relationship("AccountsPayable", back_populates="purchase_order", uselist=False)