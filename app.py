from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

app = FastAPI()

# Temporary storage (can be replaced with a real database)
fruit_inventory = []

# Fruit model
class Fruit(BaseModel):
    name: str
    variety: str
    quantity: int
    supplier: str
    harvest_date: datetime
    available: bool = True
    price: float

class FruitResponse(Fruit):
    id: str
    creation_date: datetime

# Get all available fruits
@app.get("/api/fruits", response_model=List[FruitResponse])
def get_fruits():
    return [fruit for fruit in fruit_inventory if fruit["available"]]

# Get a single fruit by ID
@app.get("/api/fruits/{fruit_id}", response_model=FruitResponse)
def get_fruit(fruit_id: str):
    fruit = next((fruit for fruit in fruit_inventory if fruit["id"] == fruit_id), None)
    if not fruit:
        raise HTTPException(status_code=404, detail="Fruit not found")
    return fruit

# Add a new fruit
@app.post("/api/fruits", response_model=FruitResponse, status_code=201)
def create_fruit(fruit: Fruit):
    fruit_data = fruit.dict()
    fruit_data["id"] = str(uuid4())
    fruit_data["creation_date"] = datetime.utcnow()
    fruit_inventory.append(fruit_data)
    return fruit_data

# Update fruit (availability, price, quantity)
@app.patch("/api/fruits/{fruit_id}", response_model=FruitResponse)
def update_fruit(fruit_id: str, available: Optional[bool] = None, price: Optional[float] = None, quantity: Optional[int] = None):
    fruit = next((fruit for fruit in fruit_inventory if fruit["id"] == fruit_id), None)
    if not fruit:
        raise HTTPException(status_code=404, detail="Fruit not found")
    
    if available is not None:
        fruit["available"] = available
    if price is not None:
        fruit["price"] = price
    if quantity is not None:
        fruit["quantity"] = quantity
    
    return fruit

# Soft delete fruit (set availability to False)
@app.delete("/api/fruits/{fruit_id}")
def delete_fruit(fruit_id: str):
    fruit = next((fruit for fruit in fruit_inventory if fruit["id"] == fruit_id), None)
    if not fruit:
        raise HTTPException(status_code=404, detail="Fruit not found")
    
    fruit["available"] = False
    return {"message": "Fruit removed from inventory"}


# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Fresh Fruit Inventory System"}


