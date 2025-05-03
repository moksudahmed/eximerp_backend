from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from app.schemas import transaction as transaction_schema
from app.models import transaction as transaction_model
from app.db.session import get_db
from app.services.CashFlowService import CashFlowService
from app.models.enum_types import AccountTypeEnum

from decimal import Decimal


router = APIRouter()


# Define the endpoint to get enum values
@router.get("/account-types", response_model=List[str])
async def get_account_types():
    return [account_type.value for account_type in AccountTypeEnum]