from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from app.schemas import vendor as vendor_schema
from app.models import vendor as vendor_model
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=vendor_schema.VendorBase)
async def create_vendor(vendor: vendor_schema.VendorCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new vendor in the database.
    """
    new_vendor = vendor_model.Vendor(**vendor.dict())
    
    try:
        db.add(new_vendor)
        await db.commit()
        await db.refresh(new_vendor)
        return new_vendor
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating vendor")

@router.get("/", response_model=List[vendor_schema.VendorResponse])
async def read_vendors(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a list of vendors with optional pagination.
    """
    stmt = select(vendor_model.Vendor).offset(skip).limit(limit)
    
    try:
        result = await db.execute(stmt)
        vendors = result.scalars().all()
        return vendors
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error retrieving vendors")