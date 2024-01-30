from fastapi import APIRouter, HTTPException, status

from models import Item
from database import fetch_item, insert_multiple_items


router = APIRouter(
  prefix="/api",
  tags=["API"],
  )

@router.get("/item/{name}", response_model=Item)
async def api_get_item(name: str):
    item = await fetch_item(name)
    if item:
        return item
    raise HTTPException(status_code=404, detail="item not found")

@router.post("/insert/", status_code=status.HTTP_201_CREATED)
async def create_multiple_items(items: list[Item]):
    result = await insert_multiple_items(items)
    if result:
        return {"message": "Items added successfully", "item_ids": result}
    raise HTTPException(status_code=400, detail="Error inserting items")