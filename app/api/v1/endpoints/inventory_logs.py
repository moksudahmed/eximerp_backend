from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from typing import List
from app.schemas import product as product_schema
from app.schemas import inventory_log as inventory_log_schema
from app.models import product as product_model
from app.models import inventory_log as inventory_model
from app.models import action_type as action
from app.db.session import get_db
from datetime import datetime
from app.schemas.purchase_order import PurchaseOrder
from app.models.purchase_order import PurchaseOrder
from sqlalchemy.orm import selectinload  # Import this for loading related objects
from sqlalchemy.exc import SQLAlchemyError
from app.models import product as product_model
router = APIRouter()


@router.post("/", response_model=inventory_log_schema.InventoryLog)
async def create_inventory_log(log: inventory_log_schema.InventoryLogCreate, db: AsyncSession = Depends(get_db)):
    # Fetch the product by ID, raise exception if not found
    try:
        product = (await db.execute(
            select(product_model.Product).filter_by(id=log.product_id)
        )).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Adjust product stock based on the action type
    if log.action_type.value == action.ActionType.ADD.value:
            product.stock += log.quantity
    elif log.action_type.value in [action.ActionType.DEDUCT.value, action.ActionType.DAMAGED.value]:            
            if product.stock < log.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for product ID {log.product_id}"
                )
            product.stock -= log.quantity       

    # No need to call product.save(), just commit the session after modifying product
    #db.add(product)  # This line may not be necessary as `product` is already tracked by the session
    
    # Create the inventory log entry
    new_log = inventory_model.InventoryLog(
        product_id=log.product_id,
        action_type=log.action_type,
        quantity=log.quantity,
        user_id = log.user_id
    )
    db.add(new_log)
    
    try:
        # Commit the transaction and refresh the log entry
        await db.commit()
        await db.refresh(new_log)  # Refresh the log to get any auto-generated fields like `id` or `created_at`
    except Exception as e:
        # Rollback the transaction in case of error
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return new_log


@router.get("/", response_model=List[inventory_log_schema.InventoryLog])
async def read_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # Use SQLAlchemy's select statement
    stmt = select(inventory_model.InventoryLog).offset(skip).limit(limit)
    
    # Execute the statement asynchronously
    result = await db.execute(stmt)
    
    # Fetch all products from the result
    inventory = result.scalars().all()
    
    return inventory

async def completed_purchase_order(order_id: int, db):
    try:
        result = await db.execute(
        select(PurchaseOrder).options(selectinload(PurchaseOrder.items)).filter_by(id=order_id))
        order = result.scalars().first()
        print("Hello World")
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


@router.post("/bulk-update", response_model=List[inventory_log_schema.InventoryLog])
async def bulk_update_inventory(
    updates: List[inventory_log_schema.InventoryLogBatchCreate],
    db: AsyncSession = Depends(get_db)
):
    """
    Bulk update inventory based on a list of inventory actions.
    """
    logs = []  # To store successfully created logs for the response
    
    for update in updates:
        try:
            # Fetch the product by ID
            product = (await db.execute(
                select(product_model.Product).filter_by(id=update.product_id)
            )).scalar_one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail=f"Product with ID {update.product_id} not found")
       
        # Adjust product stock based on action type
        #print("Test",update.action_type.value, action.ActionType.ADD.value)
        if update.action_type.value == action.ActionType.ADD.value:
            product.stock += update.quantity
        elif update.action_type.value in [action.ActionType.DEDUCT.value, action.ActionType.DAMAGED.value]:
            if product.stock < update.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for product ID {update.product_id}"
                )
            product.stock -= update.quantity       
            
        # Create an inventory log entry
        new_log = inventory_model.InventoryLog(
            product_id=update.product_id,
            action_type= update.action_type,
            quantity=update.quantity,
            user_id=update.user_id
        )      
        try:
            result = await db.execute(select(PurchaseOrder).filter(PurchaseOrder.id == update.id))
            porder = result.scalars().first()                    
            if porder.status.name == "RECEIVED":           
                porder.status = "COMPLETED"           
        except NoResultFound:
            raise HTTPException(status_code=404, detail=f"Order Status still pending.") 
        
        #completed_purchase_order(31, db) 
        db.add(new_log)
        logs.append(new_log)        

    try:
        # Commit the transaction and refresh logs
        await db.commit()
        for log in logs:
            await db.refresh(log)
    except Exception as e:
        # Rollback the transaction on failure
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return logs