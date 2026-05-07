from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Your "Fake Database"
fake_db = {}

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

# CREATE
@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    fake_db[item_id] = item
    return {"message": "Item created", "item": item}

# READ
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    item = fake_db.get(item_id)
    return {"item_id": item_id, "data": item, "q": q}

# UPDATE
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    fake_db[item_id] = item
    return {"item_name": item.name, "item_id": item_id}

# DELETE
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id in fake_db:
        del fake_db[item_id]
    return {"message": f"Item with id {item_id} has been deleted"}