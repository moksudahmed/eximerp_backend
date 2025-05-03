from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.schemas import cash_register as cash_register_schema
from app.models import cash_register as cash_register_model
from app.db.session import get_db
from typing import List
from sqlalchemy.orm import joinedload
from app.models.user import User  # Ensure this is the SQLAlchemy model

router = APIRouter()

# Create a new cash register entry
@router.post("/", response_model=cash_register_schema.CashRegister)
async def create_cash_register_entry(entry: cash_register_schema.CashRegisterCreate, db: AsyncSession = Depends(get_db)):
    # Fetch the user to verify if it exists
    result = await db.execute(select(User).filter_by(id=entry.user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create the new cash register entry
    new_entry = cash_register_model.CashRegister(
        user_id=entry.user_id,
        action_type=entry.action_type,
        amount=entry.amount,
        description=entry.description
    )
    
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)
    return new_entry

# Get all cash register entries (list all)
@router.get("/", response_model=List[cash_register_schema.CashRegister])
async def list_cash_register_entries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(cash_register_model.CashRegister).options(joinedload(cash_register_model.CashRegister.user)))
    entries = result.scalars().all()
    return entries

# Get a specific cash register entry by ID
@router.get("/cash_register/{entry_id}", response_model=cash_register_schema.CashRegister)
async def get_cash_register_entry(entry_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(cash_register_model.CashRegister).filter_by(id=entry_id))
    entry = result.scalars().first()

    if not entry:
        raise HTTPException(status_code=404, detail="Cash Register entry not found")

    return entry

# Delete a cash register entry by ID
@router.delete("/cash_register/{entry_id}")
async def delete_cash_register_entry(entry_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(cash_register_model.CashRegister).filter_by(id=entry_id))
    entry = result.scalars().first()

    if not entry:
        raise HTTPException(status_code=404, detail="Cash Register entry not found")

    await db.delete(entry)
    await db.commit()
    return {"message": "Cash Register entry deleted successfully"}

# Update a cash register entry
@router.put("/cash_register/{entry_id}", response_model=cash_register_schema.CashRegister)
async def update_cash_register_entry(entry_id: int, entry: cash_register_schema.CashRegisterCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(cash_register_model.CashRegister).filter_by(id=entry_id))
    existing_entry = result.scalars().first()

    if not existing_entry:
        raise HTTPException(status_code=404, detail="Cash Register entry not found")

    existing_entry.action_type = entry.action_type
    existing_entry.amount = entry.amount
    existing_entry.description = entry.description
    existing_entry.user_id = entry.user_id

    await db.commit()
    await db.refresh(existing_entry)
    return existing_entry
