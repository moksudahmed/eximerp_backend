from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.schemas import product as product_schema
from app.models import product as product_model
from app.db.session import get_db
from typing import List

router = APIRouter()

@router.post("/", response_model=product_schema.Product)
async def create_product(product: product_schema.ProductCreate, db: AsyncSession = Depends(get_db)):   
    db_product = product_model.Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

# PUT method to update an existing product
@router.put("/{product_id}", response_model=product_schema.Product)
async def update_product(product_id: int, product: product_schema.ProductUpdate, db: AsyncSession = Depends(get_db)):
    # Fetch the existing product from the database
    
    result = await db.execute(select(product_model.Product).filter(product_model.Product.id == product_id))
    db_product = result.scalars().first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update the product's attributes
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)

    # Commit the changes to the database
    await db.commit()
    await db.refresh(db_product)
    return db_product

@router.get("/", response_model=List[product_schema.Product])
async def read_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # Use SQLAlchemy's select statement
    stmt = select(product_model.Product).offset(skip).limit(limit)
    
    # Execute the statement asynchronously
    result = await db.execute(stmt)
    
    # Fetch all products from the result
    products = result.scalars().all()
    
    return products

# DELETE method to remove an existing product
@router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    # Fetch the existing product from the database
    result = await db.execute(select(product_model.Product).filter(product_model.Product.id == product_id))
    db_product = result.scalars().first()
   
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Delete the product from the database
    await db.delete(db_product)
    print(db_product)
    await db.commit()

    return {"detail": "Product deleted successfully"}