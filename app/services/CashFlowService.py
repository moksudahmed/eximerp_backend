from app.models import cash_flow as cashflow_model
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from app.db.session import get_db
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from decimal import Decimal

class CashFlowService:
    def __init__(self, db_session):
        self.db_session = db_session

    async def record_cash_inflow_with_transaction(
        self,
        db: AsyncSession,
        user_id: int,
        amount: float,
        description: str,
        related_transaction_id: int
    ):
        # Await the current register balance
        register_balance_before = await self.get_current_register_balance()
        
        # Convert the float amount to Decimal for precise arithmetic
        amount_decimal = Decimal(amount)
        
        # Perform the addition with Decimal types
        #register_balance_after = register_balance_before + amount_decimal
        register_balance_after = float(register_balance_before) + amount
        


        cash_flow = cashflow_model.CashFlow(
            user_id=user_id,
            action_type='CASH_INFLOW',
            amount=amount_decimal,  # Store amount as Decimal
            description=description,
            related_transaction_id=related_transaction_id,
            register_balance_before=register_balance_before,
            register_balance_after=register_balance_after
        )

        # Add the cash flow to the session
        self.db_session.add(cash_flow)
        await self.db_session.commit()  # Commit the transaction
        await self.db_session.refresh(cash_flow)  # Refreshing to get the updated state

        return cash_flow

        
    def record_cash_inflow(self, user_id, amount, description=None):
        cash_flow = cashflow_model.CashFlow(
            user_id=user_id,
            action_type='CASH_INFLOW',
            amount=amount,
            description=description,
            register_balance_before=self.get_current_register_balance(),
            register_balance_after=self.get_current_register_balance() + amount
        )
        self.db_session.add(cash_flow)
        self.db_session.commit()
        return cash_flow

    def record_cash_outflow(self, user_id, amount, description=None):
        current_balance = self.get_current_register_balance()
        if current_balance < amount:
            raise ValueError("Insufficient funds in register.")

        cash_flow = cashflow_model.CashFlow(
            user_id=user_id,
            action_type='CASH_OUTFLOW',
            amount=amount,
            description=description,
            register_balance_before=current_balance,
            register_balance_after=current_balance - amount
        )
        self.db_session.add(cash_flow)
        self.db_session.commit()
        return cash_flow

    async def get_current_register_balance(self):
        stmt = select(cashflow_model.CashFlow).order_by(cashflow_model.CashFlow.created_at.desc()).limit(1)
        
        result = await self.db_session.execute(stmt)
        last_cash_flow = result.scalars().first()  # Retrieves the first result from the query

        return last_cash_flow.register_balance_after if last_cash_flow else 0

    async def open_register(self, user_id: int, initial_amount: float, description: str):
        cash_flow = cashflow_model.CashFlow(
            user_id=user_id,
            action_type='OPEN',
            amount=initial_amount,
            description=description,
            register_balance_before=0,
            register_balance_after=initial_amount
        )
        self.db_session.add(cash_flow)
        await self.db_session.commit()
        await self.db_session.refresh(cash_flow)
        return cash_flow

    async def close_register(self, user_id, description: str):
        current_balance = await self.get_current_register_balance()
        cash_flow = cashflow_model.CashFlow(
            user_id=user_id,
            action_type='CLOSE',
            amount=current_balance,
            description=description,
            register_balance_before=current_balance,
            register_balance_after=0
        )
        self.db_session.add(cash_flow)
        #self.db_session.commit()
        await self.db_session.commit()
        await self.db_session.refresh(cash_flow)
        return cash_flow
    
   