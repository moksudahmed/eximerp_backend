from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from app.schemas import account as account_schema

from app.models import account as account_model
from app.db.session import get_db
from app.services.CashFlowService import CashFlowService
from app.models.enum_types import AccountTypeEnum

from decimal import Decimal


router = APIRouter()

@router.post("/", response_model=account_schema.Account)
async def create_account(account: account_schema.AccountCreate, db: AsyncSession = Depends(get_db)):
    new_account = account_model.Account(**account.dict())
    
    
    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)
    return new_account

# READ all transactions with pagination
@router.get("/", response_model=List[account_schema.AccountResponse])
async def read_transactions(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    stmt = select(account_model.Account).offset(skip).limit(limit)
    
    # Execute query asynchronously
    result = await db.execute(stmt)
    account = result.scalars().all()

    return account


# Get all accounts
@router.get("/accounts/", response_model=List[account_schema.AccountResponse])
def read_accounts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    accounts = db.query(account_model.Account).offset(skip).limit(limit).all()
    return accounts

# Get a single account by ID
@router.get("/accounts/{account_id}", response_model=account_schema.AccountResponse)
def read_account(account_id: int, db: AsyncSession = Depends(get_db)):
    account = db.query(account_model.Account).filter(account_model.Account.account_id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

# Update an account by ID
@router.put("/accounts/{account_id}", response_model=account_schema.AccountResponse)
def update_account(account_id: int, account: account_schema.AccountUpdate, db: AsyncSession = Depends(get_db)):
    db_account = db.query(account_model.Account).filter(account_model.Account.account_id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    for key, value in account.dict().items():
        setattr(db_account, key, value)

    db.commit()
    db.refresh(db_account)
    return db_account

# Delete an account by ID
@router.delete("/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, db: AsyncSession = Depends(get_db)):
    db_account = db.query(account_model.Account).filter(account_model.Account.account_id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db.delete(db_account)
    db.commit()
    return None

# Endpoint to get all account types (from Enum)
@router.get("/account-types/", response_model=List[str])
def get_account_types():
    return [account_type.value for account_type in AccountTypeEnum]