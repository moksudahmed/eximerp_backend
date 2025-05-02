from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4, UUID

app = FastAPI()

# ------------------------------
# Pydantic Models
# ------------------------------
class Item(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True

# ------------------------------
# Fake Database
# ------------------------------
items_db: List[Item] = []

# ------------------------------
# API Endpoints
# ------------------------------
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the FastAPI app!"}

@app.get("/items", response_model=List[Item], tags=["Items"])
def get_items():
    return items_db

@app.post("/items", response_model=Item, tags=["Items"])
def create_item(item: ItemCreate):
    new_item = Item(id=uuid4(), **item.dict())
    items_db.append(new_item)
    return new_item

@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
def get_item(item_id: UUID):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
def update_item(item_id: UUID, updated_item: ItemCreate):
    for index, item in enumerate(items_db):
        if item.id == item_id:
            updated = Item(id=item_id, **updated_item.dict())
            items_db[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", tags=["Items"])
def delete_item(item_id: UUID):
    for index, item in enumerate(items_db):
        if item.id == item_id:
            del items_db[index]
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

# ------------------------------
# For Local Testing
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
