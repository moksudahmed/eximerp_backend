from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from typing import List
from sqlalchemy.future import select
from app.schemas.journal_entry import JournalEntry, JournalEntryCreate, JournalEntryUpdate
from app.models.journal_entry import JournalEntry as JournalEntryModel
from sqlalchemy.orm import selectinload  # Import this for loading related objects

router = APIRouter()

# Get all journal entries
@router.get("/", response_model=List[JournalEntry])
async def get_journal_entries(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(JournalEntryModel).offset(skip).limit(limit)
    )
    return result.scalars().all()

# Get a single journal entry by ID
@router.get("/{entry_id}", response_model=JournalEntry)
async def get_journal_entry(entry_id: int, db: AsyncSession = Depends(get_db)):
    entry = await db.get(JournalEntryModel, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    return entry

# Get a single journal entry by ID
@router.get("/account/{account_id}", response_model=list[JournalEntry]) 
async def get_journal_entries(account_id: int, db: AsyncSession = Depends(get_db)):   
    result = await db.execute(
        select(JournalEntryModel)
        .options(selectinload(JournalEntryModel.account))
        .filter(JournalEntryModel.account_id == account_id)
    )
    accounts = result.scalars().all()  
    if not accounts:
        raise HTTPException(status_code=404, detail="No journal entries found for the given account_id")
    return accounts

# Create a new journal entry
@router.post("/journal-entries/", response_model=JournalEntry)
async def create_journal_entry(entry_data: JournalEntryCreate, db: AsyncSession = Depends(get_db)):
    new_entry = JournalEntryModel(**entry_data.dict())
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)
    return new_entry

# Update an existing journal entry
@router.put("/journal-entries/{entry_id}", response_model=JournalEntry)
async def update_journal_entry(entry_id: int, entry_data: JournalEntryUpdate, db: AsyncSession = Depends(get_db)):
    entry = await db.get(JournalEntryModel, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    
    for key, value in entry_data.dict(exclude_unset=True).items():
        setattr(entry, key, value)
    
    await db.commit()
    await db.refresh(entry)
    return entry

# Delete a journal entry
@router.delete("/journal-entries/{entry_id}")
async def delete_journal_entry(entry_id: int, db: AsyncSession = Depends(get_db)):
    entry = await db.get(JournalEntryModel, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    
    await db.delete(entry)
    await db.commit()
    return {"detail": "Journal entry deleted"}
