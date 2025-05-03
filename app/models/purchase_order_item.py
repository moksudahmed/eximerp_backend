from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from enum import Enum
from datetime import date
from app.models.enum_types import OrderStatusEnum
from app.db.base import Base

class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"
    id = Column(Integer, primary_key=True)
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    cost_per_unit = Column(Float, nullable=False)

    purchase_order = relationship("PurchaseOrder", back_populates="items")
