from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import cash_flow as cashflow_schema
from app.models import cash_flow as cash_flow_model
from app.db.session import get_db
from app.services.CashFlowService import CashFlowService
from typing import List

router = APIRouter()


# Helper function to get CashFlowService
def get_cashflow_service(db: AsyncSession = Depends(get_db)):
    return CashFlowService(db)

# CREATE a new cash inflow record
@router.post("/inflow/", response_model=cashflow_schema.CashFlow)
async def record_cash_inflow(
    user_id: int,
    amount: float,
    description: str = None,
    cashflow_service: CashFlowService = Depends(get_cashflow_service)
):
    try:
        cashflow = cashflow_service.record_cash_inflow(user_id, amount, description)
        return cashflow
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# CREATE a new cash outflow record
@router.post("/outflow/", response_model=cashflow_schema.CashFlow)
async def record_cash_outflow(
    user_id: int,
    amount: float,
    description: str = None,
    cashflow_service: CashFlowService = Depends(get_cashflow_service)
):
    try:
        cashflow = cashflow_service.record_cash_outflow(user_id, amount, description)
        return cashflow
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# OPEN registerXHRPOST
# OPEN register

@router.post("/open-register", response_model=cashflow_schema.CashFlow)
async def open_register(
    request: cashflow_schema.OpenRegisterRequest,  # Request body
    cashflow_service: CashFlowService = Depends(get_cashflow_service)
):
    print("Hello World Open Register")
    # Pass the request body parameters to the service method
    cashflow = await cashflow_service.open_register(
        user_id=request.user_id, 
        initial_amount=request.amount, 
        description=request.description or ''  # Ensure description is not None
    )
    return cashflow

@router.get("/register-status")
async def get_register_status(db: AsyncSession = Depends(get_db)):
    # Query to find the latest cash register actions
    result = await db.execute(select(cash_flow_model.CashFlow)
                              .order_by(cash_flow_model.CashFlow.created_at.desc())
                              .limit(1))
    last_cash_flow = result.scalars().first()

    if not last_cash_flow:
        return {"status": "No register actions found"}

    # Check if the register is open by looking for the last "OPEN" action and ensuring it hasn't been closed
    if last_cash_flow.action_type == "CLOSE":
        status = "closed"
    else:
        # Query to check if there was an "OPEN" action that hasn't been followed by a "CLOSE" action
        result_open = await db.execute(select(cash_flow_model.CashFlow)
                                       .where(cash_flow_model.CashFlow.action_type == "OPEN")
                                       .order_by(cash_flow_model.CashFlow.created_at.desc())
                                       .limit(1))
        last_open_action = result_open.scalars().first()

        if last_open_action:
            # Ensure there's no subsequent "CLOSE" action
            result_close = await db.execute(select(cash_flow_model.CashFlow)
                                            .where(cash_flow_model.CashFlow.action_type == "CLOSE")
                                            .order_by(cash_flow_model.CashFlow.created_at.desc())
                                            .limit(1))
            last_close_action = result_close.scalars().first()

            if not last_close_action or last_close_action.created_at < last_open_action.created_at:
                status = "open"
            else:
                status = "closed"
        else:
            status = "closed"

    return {
        "status": status,
        "register_balance": last_cash_flow.register_balance_after,
        "last_action": last_cash_flow.action_type,
        "last_updated": last_cash_flow.created_at
    }

@router.get("/register-status2")
async def get_register_status2(db: AsyncSession = Depends(get_db)):
    # Query to find the latest cash register status
    result = await db.execute(select(cash_flow_model.CashFlow).order_by(cash_flow_model.CashFlow.created_at.desc()).limit(1))
    last_cash_flow = result.scalars().first()

    if not last_cash_flow:
        return {"status": "No register actions found"}

    # Determine the status based on the last action
    status = "open" if last_cash_flow.action_type == "OPEN" else "closed"
    
    return {
        "status": status,
        "register_balance": last_cash_flow.register_balance_after,
        "last_action": last_cash_flow.action_type,
        "last_updated": last_cash_flow.created_at
    }
# CLOSE register

@router.post("/close-register", response_model=cashflow_schema.CashFlow)
async def close_register(
    request: cashflow_schema.CloseRegisterRequest,  # Request body
    cashflow_service: CashFlowService = Depends(get_cashflow_service)
):
    # Pass the request body parameters to the service method
    print("Hello World")
    cashflow = await cashflow_service.close_register(
        user_id=request.user_id, 
        description=request.description or ''  # Ensure description is not None
    )
    return cashflow


# GET all cashflow records (with pagination)
@router.get("/", response_model=List[cashflow_schema.CashFlow])
async def read_cashflows(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    stmt = select(cash_flow_model.CashFlow).offset(skip).limit(limit)
    
    # Execute query asynchronously
    result = await db.execute(stmt)
    cashflows = result.scalars().all()

    return cashflows

# CREATE a new cash flow record (inflow or outflow)
@router.post("/", response_model=cashflow_schema.CashFlow)
async def create_cashflow(cashflow: cashflow_schema.CashFlowCreate, db: AsyncSession = Depends(get_db)):
    db_cashflow = cash_flow_model.CashFlow(**cashflow.dict())
    db.add(db_cashflow)
    await db.commit()
    await db.refresh(db_cashflow)
    return db_cashflow

# UPDATE an existing cash flow record
@router.put("/{cashflow_id}", response_model=cashflow_schema.CashFlow)
async def update_cashflow(cashflow_id: int, cashflow: cashflow_schema.CashFlowUpdate, db: AsyncSession = Depends(get_db)):
    # Fetch the existing cash flow record
    result = await db.execute(select(cash_flow_model.CashFlow).filter(cash_flow_model.CashFlow.id == cashflow_id))
    db_cashflow = result.scalars().first()

    if not db_cashflow:
        raise HTTPException(status_code=404, detail="Cash flow record not found")

    # Update the cash flow record's attributes
    for key, value in cashflow.dict(exclude_unset=True).items():
        setattr(db_cashflow, key, value)

    # Commit changes to the database
    await db.commit()
    await db.refresh(db_cashflow)
    return db_cashflow

# READ all cash flow records with pagination
@router.get("/", response_model=List[cashflow_schema.CashFlow])
async def read_cashflows(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    stmt = select(cash_flow_model.CashFlow).offset(skip).limit(limit)
    
    # Execute query asynchronously
    result = await db.execute(stmt)
    cashflows = result.scalars().all()

    return cashflows

# DELETE an existing cash flow record
@router.delete("/{cashflow_id}", response_model=dict)
async def delete_cashflow(cashflow_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(cash_flow_model.CashFlow).filter(cash_flow_model.CashFlow.id == cashflow_id))
    db_cashflow = result.scalars().first()

    if not db_cashflow:
        raise HTTPException(status_code=404, detail="Cash flow record not found")

    # Delete the cash flow record
    await db.delete(db_cashflow)
    await db.commit()

    return {"detail": "Cash flow record deleted successfully"}
