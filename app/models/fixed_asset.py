from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, Enum, Boolean, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base


class FixedAsset(Base):
    __tablename__ = 'fixed_assets'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    value = Column(Numeric(10, 2), nullable=False)
    depreciation_rate = Column(Numeric(10, 2), nullable=False)
    purchased_date = Column(DateTime, nullable=False)
    status = Column(Boolean, default=True)  # Active or Inactive
