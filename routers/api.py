from fastapi import APIRouter, HTTPException

from models import Item
from database import fetch_item


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
