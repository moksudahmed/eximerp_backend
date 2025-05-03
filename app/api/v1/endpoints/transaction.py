from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from app.schemas import transaction as transaction_schema
from app.models import transaction as transaction_model
from app.db.session import get_db
from app.services.CashFlowService import CashFlowService
from app.models import cash_flow as cashflow_model
from decimal import Decimal


import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# Helper function to get CashFlowService
def get_cashflow_service(db: AsyncSession = Depends(get_db)):
    return CashFlowService(db)

# CREATE a new transaction
@router.post("/", response_model=transaction_schema.Transaction)
async def create_transaction(transaction: transaction_schema.TransactionCreate, db: AsyncSession = Depends(get_db)):
    db_transaction = transaction_model.Transaction(**transaction.dict())
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

# UPDATE an existing transaction
@router.put("/{transaction_id}", response_model=transaction_schema.Transaction)
async def update_transaction(transaction_id: int, transaction: transaction_schema.TransactionUpdate, db: AsyncSession = Depends(get_db)):
    # Fetch the existing transaction
    result = await db.execute(select(transaction_model.Transaction).filter(transaction_model.Transaction.id == transaction_id))
    db_transaction = result.scalars().first()

    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Update the transaction's attributes
    for key, value in transaction.dict(exclude_unset=True).items():
        setattr(db_transaction, key, value)

    # Commit changes to the database
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

# READ all transactions with pagination
@router.get("/", response_model=List[transaction_schema.Transaction])
async def read_transactions(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    stmt = select(transaction_model.Transaction).offset(skip).limit(limit)
    
    # Execute query asynchronously
    result = await db.execute(stmt)
    transactions = result.scalars().all()

    return transactions

# DELETE an existing transaction
@router.delete("/{transaction_id}", response_model=dict)
async def delete_transaction(transaction_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(transaction_model.Transaction).filter(transaction_model.Transaction.id == transaction_id))
    db_transaction = result.scalars().first()

    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Delete the transaction
    await db.delete(db_transaction)
    await db.commit()

    return {"detail": "Transaction deleted successfully"}


def get_cashflow_service(db: AsyncSession = Depends(get_db)):
    return CashFlowService(db)

@router.post("/transaction_with_inflow/", response_model=transaction_schema.Transaction)
async def create_transaction_with_inflow(
    transaction: transaction_schema.TransactionCreate,
    db: AsyncSession = Depends(get_db),
    cashflow_service: CashFlowService = Depends(get_cashflow_service)
):
    try:
        async with db.begin():  # Start a database transaction
            # 1. Create the transaction and add it to the session
            db_transaction = transaction_model.Transaction(**transaction.dict())
            db.add(db_transaction)
            await db.flush()  # Flush the transaction to get the ID

            # 2. Convert to Pydantic schema before committing
            response_transaction = transaction_schema.Transaction.from_orm(db_transaction)

            # 3. Get the transaction ID for linking to cash flow
            related_transaction_id = db_transaction.id

            user_id = transaction.user_id
            amount_decimal = Decimal(transaction.amount)  # Convert amount to Decimal
            description = transaction.description or f"Inflow for transaction {related_transaction_id}"

            # 4. Calculate register balance before and after
            register_balance_before = await cashflow_service.get_current_register_balance()
            register_balance_after = register_balance_before + amount_decimal

            # 5. Create the cash inflow record
            cash_flow = cashflow_model.CashFlow(
                user_id=user_id,
                action_type='CASH_INFLOW',
                amount=amount_decimal,
                description=description,
                related_transaction_id=related_transaction_id,
                register_balance_before=register_balance_before,
                register_balance_after=register_balance_after
            )

            # 6. Add the cash flow record to the session
            db.add(cash_flow)
            await db.flush()  # Flush the cash flow record

            # 7. Commit the transaction and cash flow together
            await db.commit()

            # 8. Return the pre-committed transaction object
            return response_transaction

    except Exception as e:
        # Log the detailed exception for debugging
        logger.error(f"Transaction failed due to: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Transaction failed due to an internal error: {str(e)}")
