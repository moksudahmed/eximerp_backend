from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.purchase_order import PurchaseOrder
from app.models.purchase_order_item import PurchaseOrderItem
from app.models.accounts_payable import AccountsPayable
#from app.models.payment_transactions import PaymentTransaction
from app.schemas.purchase_order import PurchaseOrder
from app.models.purchase_order import PurchaseOrder
from app.schemas import purchase_order as purchase_order_schema
from app.models import product as product_model
from app.db.session import get_db
from typing import List
from sqlalchemy.orm import selectinload  # Import this for loading related objects

router = APIRouter()

@router.post("/", response_model=purchase_order_schema.PurchaseOrderResponse)
async def create_purchase_order(
    order_data: purchase_order_schema.PurchaseOrderCreate, 
    db: AsyncSession = Depends(get_db)
):
    try:
        # Create the purchase order
        new_order = PurchaseOrder(
            vendor_id=order_data.vendor_id,
            date=order_data.date,
            total_amount=order_data.total_amount,
            status=order_data.status,
            user_id=order_data.user_id
        )
        
        #await db.flush()

        # Add items to the purchase order
        for item_data in order_data.items:
            item = PurchaseOrderItem(               
                product_id=item_data.product_id,
                quantity=item_data.quantity,
                cost_per_unit=item_data.cost_per_unit,
                purchase_order=new_order
            )
            db.add(item)
          # Create accounts payable entry
        accounts_payable = AccountsPayable(
            purchase_order_id=new_order.id,
            amount_due=new_order.total_amount,
            amount_paid=0.0
        )
        
        db.add(accounts_payable)
        db.add(new_order)
        await db.commit()         
        await db.refresh(new_order)
        #return new_order
        # Query and return the created ledger with linked journal entries
        result = await db.execute(
            select(PurchaseOrder).options(selectinload(PurchaseOrder.items)).filter_by(id=new_order.id)
        )
        new_order = result.scalars().first()
        
        return new_order
    
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/abc", response_model=purchase_order_schema.PurchaseOrderResponse)
async def create_purchase_order2(order_data: purchase_order_schema.PurchaseOrderCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Create the purchase order
        new_order = PurchaseOrder(
            vendor_id=order_data.vendor_id,
            date=order_data.date,
            total_amount=order_data.total_amount,
            status=order_data.status,  # Convert to lowercase
            user_id=order_data.user_id
        )
        db.add(new_order)
        await db.flush()

        # Add items to the purchase order
        for item_data in order_data.items:
            item = PurchaseOrderItem(
                purchase_order_id=new_order.id,
                product_id=item_data.product_id,
                quantity=item_data.quantity,
                cost_per_unit=item_data.cost_per_unit
            )
            db.add(item)

        # Create accounts payable entry
      #  accounts_payable = AccountsPayable(
       #     purchase_order_id=new_order.id,
       #     amount_due=new_order.total_amount,
       #     amount_paid=0.0
       # )
       # db.add(accounts_payable)

        await db.commit()
        await db.refresh(new_order)
        return new_order
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/", response_model=List[purchase_order_schema.PurchaseOrderResponse])
async def get_purchase_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PurchaseOrder).options(selectinload(PurchaseOrder.items)))
    sales = result.scalars().all()
    return sales

# Get details of a specific purchase order
@router.get("/{order_id}", response_model=purchase_order_schema.PurchaseOrderResponse)
async def get_purchase_order(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PurchaseOrder).options(selectinload(PurchaseOrder.items)).filter_by(id=order_id)
    )
    order = result.scalars().first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

# Mark a purchase order as received
@router.post("/{order_id}/receive")
async def receive_purchase_order(order_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
        select(PurchaseOrder).options(selectinload(PurchaseOrder.items)).filter_by(id=order_id))
        order = result.scalars().first()
        
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        if order.status.name != "PENDING":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order cannot be received")

        order.status = "RECEIVED"
       
        await db.commit()
        await db.refresh(order)
        return {"message": "Order received successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Mark a purchase order as cancelled
@router.post("/{order_id}/cancel")
async def cancel_purchase_order(order_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
        select(PurchaseOrder).options(selectinload(PurchaseOrder.items)).filter_by(id=order_id))
        order = result.scalars().first()
        
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        if order.status.name == "COMPLETED":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Completed orders cannot be cancelled")

        order.status = "CANCELLED"
        await db.commit()
        await db.refresh(order)
        return {"message": "Order cancelled successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
# Mark a purchase order as completed
@router.post("/{order_id}/completed")
async def completed_purchase_order(order_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
        select(PurchaseOrder).options(selectinload(PurchaseOrder.items)).filter_by(id=order_id))
        order = result.scalars().first()
        
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        if order.status.name != "RECEIVED":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Completed orders cannot be cancelled")
        order.status = "COMPLETED"
        
        await db.commit()
        await db.refresh(order)
        return {"message": "Order completed successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Mark a purchase order as received

@router.get("/received/", response_model=List[purchase_order_schema.PurchaseOrderResponse])
async def get_received_order(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PurchaseOrder).options(selectinload(PurchaseOrder.items)).filter_by(status='RECEIVED'))
    sales = result.scalars().all()
    return sales