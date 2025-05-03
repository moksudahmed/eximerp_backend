from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import general_ledger as general_ledger_schema
from app.models.general_ledger import GeneralLedger
from app.models.journal_entry import JournalEntry
from app.schemas.general_ledger import LedgerWithEntryRequest
from app.schemas.general_ledger import (
    GeneralLedgerCreate, GeneralLedgerUpdate, GeneralLedger as GeneralLedgerSchema
)
from app.schemas.journal_entry import (
    JournalEntryCreate, JournalEntryUpdate, JournalEntry as JournalEntrySchema
)
from typing import List
from sqlalchemy.orm import selectinload  # Import this for loading related objects
from sqlalchemy import text

router = APIRouter()
@router.post("/ledger-with-entry/", status_code=status.HTTP_201_CREATED)
async def create_ledger_with_entry(
    entry_data: LedgerWithEntryRequest, db: AsyncSession = Depends(get_db)
):
    # Extract general ledger data
    #general_ledger_data = entry_data.general_ledger

    # Create new General Ledger entry
    new_ledger = GeneralLedger(
        ref_no=entry_data.ref_no,
        account_type=entry_data.account_type.value.lower(),  # Convert to lowercase
        company=entry_data.company,
        transaction_date=entry_data.transaction_date,
        user_id=entry_data.user_id
    )

    # Add journal entries linked to the ledger
    for journal in entry_data.journal_entries:
        new_entry = JournalEntry(
            narration=journal.narration,
            debitcredit=journal.debitcredit,
            amount=journal.amount,
            account_id=journal.account_id,
            general_ledger=new_ledger  # Link to the ledger
        )
        db.add(new_entry)

    # Save and commit new ledger and entries
    db.add(new_ledger)
    await db.commit()
    await db.refresh(new_ledger)

    # Query and return the created ledger with linked journal entries
    result = await db.execute(
        select(GeneralLedger).options(selectinload(GeneralLedger.journal_entries)).filter_by(id=new_ledger.id)
    )
    created_ledger = result.scalars().first()

    return {
        "general_ledger": created_ledger,
        "journal_entries": created_ledger.journal_entries  # Return all linked journal entries
    }

@router.post("/general-ledger/", response_model=GeneralLedgerSchema, status_code=status.HTTP_201_CREATED)
async def create_general_ledger(
    ledger: GeneralLedgerCreate, db: AsyncSession = Depends(get_db)
):
    new_ledger = GeneralLedger(
        account_name=ledger.account_name,
        account_type=ledger.account_type.value.lower(),  # Convert to lowercase before saving
        debit=ledger.debit,
        credit=ledger.credit,
        user_id=ledger.user_id
    )
    db.add(new_ledger)
    await db.commit()
    await db.refresh(new_ledger)
    return new_ledger

@router.post("/general-ledger-journals/", response_model=GeneralLedgerSchema, status_code=status.HTTP_201_CREATED)
async def create_general_ledger_with_journals(
    ledger: GeneralLedgerCreate, db: AsyncSession = Depends(get_db)
):
    new_ledger = GeneralLedger(
        account_name=ledger.account_name,
        account_type=ledger.account_type.value.lower(),  # Convert to lowercase before saving
        debit=ledger.debit,
        credit=ledger.credit,
        user_id=ledger.user_id
    )

    
    db.add(new_ledger)
    await db.commit()
    await db.refresh(new_ledger)
    return new_ledger


@router.get("/general-ledger/", response_model=List[general_ledger_schema.GeneralLedger])
async def get_general_ledger(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(GeneralLedger).options(selectinload(GeneralLedger.journal_entries)))
    ledger = result.scalars().all()
    return ledger



@router.get("/journal-entries/", response_model=List[JournalEntrySchema])
async def get_journal_entry_list(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JournalEntry).options(selectinload(JournalEntry.general_ledger)))
    journals = result.scalars().all()
    return journals


@router.get("/general-ledger/{ledger_id}", response_model=GeneralLedgerSchema)
async def get_general_ledger(ledger_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(GeneralLedger).filter(GeneralLedger.id == ledger_id))
    ledger = result.scalars().first()
    if not ledger:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="General Ledger not found")
    return ledger


@router.put("/general-ledger/{ledger_id}", response_model=GeneralLedgerSchema)
async def update_general_ledger(
    ledger_id: int, ledger_update: GeneralLedgerUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(GeneralLedger).filter(GeneralLedger.id == ledger_id))
    ledger = result.scalars().first()
    if not ledger:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="General Ledger not found")

    ledger.account_name = ledger_update.account_name or ledger.account_name
    ledger.account_type = ledger_update.account_type or ledger.account_type
    ledger.debit = ledger_update.debit or ledger.debit
    ledger.credit = ledger_update.credit or ledger.credit

    db.add(ledger)
    await db.commit()
    await db.refresh(ledger)
    return ledger


@router.delete("/general-ledger/{ledger_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_general_ledger(ledger_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(GeneralLedger).filter(GeneralLedger.id == ledger_id))
    ledger = result.scalars().first()
    if not ledger:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="General Ledger not found")
    
    await db.delete(ledger)
    await db.commit()
    return {"message": "General Ledger deleted successfully"}


# Journal Entry Endpoints
@router.post("/journal-entries/", response_model=JournalEntrySchema, status_code=status.HTTP_201_CREATED)
async def create_journal_entry(
    entry: JournalEntryCreate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(GeneralLedger).filter(GeneralLedger.id == entry.general_ledger_id))
    general_ledger = result.scalars().first()
    if not general_ledger:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="General Ledger not found")

    new_entry = JournalEntry(
        entry_type=entry.entry_type,        
        debit=entry.debit,  # Use debit instead of amount
        credit=entry.credit,  # Add credit to the entry
        description=entry.description,     
        transaction_date= entry.transaction_date,  # Add transaction date
        general_ledger_id= entry.general_ledger_id
    )

    
    
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)
    return new_entry

@router.get("/journal-entries/{entry_id}", response_model=JournalEntrySchema)
async def get_journal_entry(entry_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JournalEntry).filter(JournalEntry.id == entry_id))
    entry = result.scalars().first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journal Entry not found")
    return entry


@router.put("/journal-entries/{entry_id}", response_model=JournalEntrySchema)
async def update_journal_entry(
    entry_id: int, entry_update: JournalEntryUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(JournalEntry).filter(JournalEntry.id == entry_id))
    entry = result.scalars().first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journal Entry not found")

    entry.entry_type = entry_update.entry_type or entry.entry_type
    entry.amount = entry_update.amount or entry.amount
    entry.description = entry_update.description or entry.description

    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry


@router.delete("/journal-entries/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_journal_entry(entry_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JournalEntry).filter(JournalEntry.id == entry_id))
    entry = result.scalars().first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journal Entry not found")

    await db.delete(entry)
    await db.commit()
    return {"message": "Journal Entry deleted successfully"}

@router.get("/ledger-summary/", status_code=status.HTTP_200_OK)
async def get_summary(db: AsyncSession = Depends(get_db)):
    sql = text('SELECT g.account_type, sum(journal_entries.amount) FROM public.general_ledger g, public.journal_entries WHERE g.id = journal_entries.general_ledger_id GROUP BY g.account_type')
    result = await db.execute(sql)
    rows = result.fetchall()

    # Retrieve column names from the result's metadata
    column_names = result.keys()

    # Convert each row to a dictionary
    ledger_entries = [dict(zip(column_names, row)) for row in rows]

    return {"ledger_entries": ledger_entries}