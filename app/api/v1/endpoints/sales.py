from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.schemas import sale as sale_schema
from app.models import sale as sale_model
from app.models.sale import Sale  # Make sure to import the Sale model
from app.models import product as product_model
from app.db.session import get_db
from typing import List
from sqlalchemy import select, delete
from sqlalchemy.future import select
from app.models.product import Product
from app.models.sale import Sale
from app.models.sale_product import SaleProduct
from app.models.user import User
from sqlalchemy.orm import selectinload  # Import this for loading related objects
from app.schemas.sale import SaleCreate, SaleUpdate, Sale as SaleSchema
from app.models import inventory_log as inventory_model
router = APIRouter()

@router.post("/", response_model=SaleSchema)
async def create_sale(sale: SaleCreate, db: AsyncSession = Depends(get_db)):
    # Initialize a new Sale object
    db_sale = Sale(user_id=sale.user_id,customer_id=sale.customer_id, total=sale.total, discount=sale.discount)
   
    for sale_product in sale.sale_products:
        product = await db.get(Product, sale_product.product_id)
        
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {sale_product.product_id} not found")
        
        if product.stock < sale_product.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product with id {sale_product.product_id}")
        
        # Create the SaleProduct record
        db_sale_product = SaleProduct(
            product_id=sale_product.product_id,
            quantity=sale_product.quantity,
            unit_price = sale_product.unit_price, 
            total_price=sale_product.total_price,
            #itemwise_discount=sale_product.itemwise_discount,
            sale=db_sale  # Link this SaleProduct to the Sale
        )
        
        # Update the stock of the product
        product.stock -= sale_product.quantity
        db.add(db_sale_product)
        
        new_log = inventory_model.InventoryLog(
            product_id=sale_product.product_id,
            action_type='DEDUCT',
            quantity=sale_product.quantity,
            user_id = 1
        )
        db.add(new_log)
    
    db.add(db_sale)
    await db.commit()
    await db.refresh(db_sale)
    
    # Ensure sale_products are loaded with selectinload
    result = await db.execute(
        select(Sale).options(selectinload(Sale.sale_products)).filter_by(id=db_sale.id)
    )
    db_sale = result.scalars().first()
    
    return db_sale

@router.put("/{sale_id}", response_model=SaleSchema)
async def update_sale(sale_id: int, sale: SaleUpdate, db: AsyncSession = Depends(get_db)):
    # Fetch the existing sale
    print("Update sale: ")
    print(sale)
    result = await db.execute(
        select(Sale).options(selectinload(Sale.sale_products)).filter_by(id=sale_id)
    )
    db_sale = result.scalars().first()
    
    if not db_sale:
        raise HTTPException(status_code=404, detail=f"Sale with id {sale_id} not found")
    
    # Update sale's total and user_id if provided
    if sale.total is not None:
        db_sale.total = sale.total
    if sale.user_id is not None:
        db_sale.user_id = sale.user_id
    if sale.discount is not None:
        db_sale.discount = sale.discount
    # Process sale products
    for sale_product_data in sale.sale_products:
        # Check if the product exists
        product = await db.get(Product, sale_product_data.product_id)
        
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {sale_product_data.product_id} not found")
        
        # Find the existing SaleProduct or create a new one
        db_sale_product = next((sp for sp in db_sale.sale_products if sp.product_id == sale_product_data.product_id), None)
        
        if db_sale_product:
            # Update the existing SaleProduct
            product.stock += db_sale_product.quantity  # Revert stock change
            if product.stock < sale_product_data.quantity:
                raise HTTPException(status_code=400, detail=f"Not enough stock for product with id {sale_product_data.product_id}")
            
            product.stock -= sale_product_data.quantity
            db_sale_product.quantity = sale_product_data.quantity
            db_sale_product.total_price = sale_product_data.total_price
            #db_sale_product.itemwise_discount = sale_product_data.itemwise_discount
        else:
            # Create a new SaleProduct record
            if product.stock < sale_product_data.quantity:
                raise HTTPException(status_code=400, detail=f"Not enough stock for product with id {sale_product_data.product_id}")
            
            product.stock -= sale_product_data.quantity
            
            new_sale_product = SaleProduct(
                product_id=sale_product_data.product_id,
                quantity=sale_product_data.quantity,
                total_price=sale_product_data.total_price,
                #itemwise_discount = sale_product_data.itemwise_discount,
                sale=db_sale  # Link this SaleProduct to the Sale
            )
            db.add(new_sale_product)
    
    await db.commit()
    await db.refresh(db_sale)
    
    # Ensure sale_products are loaded with selectinload
    result = await db.execute(
        select(Sale).options(selectinload(Sale.sale_products)).filter_by(id=db_sale.id)
    )
    db_sale = result.scalars().first()
    
    return db_sale

@router.get("/", response_model=List[sale_schema.Sale])
async def get_sales(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Sale).options(selectinload(Sale.sale_products)))
    sales = result.scalars().all()
    return sales

@router.delete("/{sale_id}", response_model=sale_schema.Sale)
async def delete_sale(sale_id: int, db: AsyncSession = Depends(get_db)):
    # Fetch the sale
    result = await db.execute(
        select(Sale).options(selectinload(Sale.sale_products)).filter_by(id=sale_id)
    )
    db_sale = result.scalars().first()

    if not db_sale:
        raise HTTPException(status_code=404, detail=f"Sale with id {sale_id} not found")

    # Revert the stock of each product and delete SaleProduct records
    for sale_product in db_sale.sale_products:
        product = await db.get(Product, sale_product.product_id)
        if product:
            product.stock += sale_product.quantity
        await db.execute(delete(SaleProduct).where(SaleProduct.id == sale_product.id))

    # Delete the sale
    await db.delete(db_sale)
    await db.commit()

    return db_sale