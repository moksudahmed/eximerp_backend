from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base
from sqlalchemy.sql import func

from sqlalchemy import Enum
import enum
from app.models.enum_types import ActionType

    
class InventoryLog(Base):
    __tablename__ = 'inventory_log'
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    action_type = Column(Enum(ActionType, name="actiontype"), nullable=False)
    quantity = Column(Integer, nullable=False) 
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    product = relationship("Product", back_populates="inventory_log")
    users = relationship("User", back_populates="inventory_log")

    #product = relationship("Product")

