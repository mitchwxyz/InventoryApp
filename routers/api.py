from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status

from models import Item
from database import fetch_item, insert_multiple_items, get_all_items, cleanup_old_records


router = APIRouter(
  prefix="/api",
  tags=["API"],
  )


@router.get("/items", response_model=list[Item])
async def get_all(user_id: str):
    """
    Retrieve a list of all items in the database.

    Returns:
        list[Item]: A list of items, each item is an instance of the Item model.
    """
    items = await get_all_items(user_id)
    return items


@router.get("/item/{item_id}", response_model=Item)
async def api_get_item(item_id: str):
    """
    Retrieve a single item by its name.

    Args:
        name (str): The name of the item to be retrieved.

    Returns:
        Item: An item instance matching the given name.

    Raises:
        HTTPException: 404 error if the item is not found in the database.
    """
    item = await fetch_item(item_id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="item not found")


@router.post("/insert/", status_code=status.HTTP_201_CREATED)
async def create_multiple_items(items: list[Item], user_id: str):
    """
    Insert multiple items into the database.

    Args:
        items (list[Item]): A list of item instances to be inserted into the database.

    Returns:
        dict: A message confirming the successful addition of items and their IDs.

    Raises:
        HTTPException: 400 error if there is an error inserting the items.
    """
    new_items = []
    update_fields = {"update_date": datetime.now(),
                     "user_id": user_id,
                    }
    for item in items:
        new_item = item.model_copy(update=update_fields)
        new_items.append(new_item)
    result = await insert_multiple_items(new_items)
    if result:
        return {"message": "Items added successfully", "item_ids": result}
    raise HTTPException(status_code=400, detail="Error inserting items")

@router.post("/cleanup")
async def cleanup_old():
    two_weeks = datetime.now() - timedelta(weeks=2)
    await cleanup_old_records(two_weeks)
    return {"message": "Old Item removed"}