from datetime import datetime

from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, Response

from database import fetch_inventory_page, fetch_item, add_item, update_item, delete_item, search_items
from models import Item, UpdateItem, Input_Types
from utils.user_cookies import get_user, set_user


router = APIRouter(
    prefix="/app",
    tags=["App"],
    include_in_schema=False,
)

templates = Jinja2Templates(directory="templates")
item_schema = Item.model_json_schema()

ITEMS_PER_PAGE = 30


@router.get("/")
async def get_inventory(request: Request, page: int = 1, user_id: str = Depends(get_user)):
    """
    Fetch a page of inventory items and render it using the 'base.html' template.

    Args:
        request (Request): The HTTP request object.
        page (int, optional): The page number for pagination. Defaults to 1.

    Returns:
        TemplateResponse: A template response with the current page of inventory items.
    """
    items = await fetch_inventory_page(page, ITEMS_PER_PAGE, user_id)
    response = templates.TemplateResponse("base.html", {"request": request,
                                                    "item_schema": item_schema,
                                                    "input_types": Input_Types,
                                                    "items": items,
                                                    "current_page": 1,
                                                    })
    await set_user(response, user_id)
    return response


@router.get("/items")
async def more_inventory(request: Request, page: int, search: str, user_id: str = Depends(get_user)):
    """
    Fetch a page of inventory items with an optional search query and render it using the 'more_rows.html' template.

    Args:
        request (Request): The HTTP request object.
        page (int): The page number for pagination.
        search (str, optional): Search query to filter items. Defaults to None.

    Returns:
        TemplateResponse: A template response with a list of items matching the search query and pagination details.
    """
    clean_search = "" if search == "None" else search
    if clean_search:
        items = await search_items(clean_search, page, ITEMS_PER_PAGE, user_id)
    else:
        items = await fetch_inventory_page(page, ITEMS_PER_PAGE, user_id)
        response = templates.TemplateResponse("more_rows.html", {"request": request,
                                                         "item_schema": item_schema,
                                                         "items": items,
                                                         "current_page":page,
                                                         "search": clean_search})
        await set_user(response, user_id)
    return response


@router.get("/item/{item_id}")
async def get_item(request: Request, item_id: str, user_id: str = Depends(get_user)):
    """
    Fetch a single item by its ID and render it using the 'view_item_row.html' template.

    Args:
        request (Request): The HTTP request object.
        item_id (str): The unique identifier of the item.

    Returns:
        TemplateResponse: A template response with details of the requested item.
    """
    item = await fetch_item(item_id)
    response = templates.TemplateResponse("view_item_row.html", {"request": request,
                                                            "item_schema": item_schema,
                                                             "item": item})
    await set_user(response, user_id)
    return response


@router.post("/search")
async def search_name(request: Request, search: str = Form(None), user_id: str = Depends(get_user)):
    """
    Perform a search operation on inventory items and render the results using the 'inventory.html' template.

    Args:
        request (Request): The HTTP request object.
        search (str, optional): The search query string. Defaults to None.

    Returns:
        TemplateResponse: A template response with the search results.
    """
    if search:
        items = await search_items(search, 1, ITEMS_PER_PAGE, user_id)
    else: items = await fetch_inventory_page(1, ITEMS_PER_PAGE, user_id)
    response = templates.TemplateResponse("inventory.html", {"request": request,
                                                         "item_schema": item_schema,
                                                         "items": items,
                                                         "current_page": 1,
                                                         "search": search})
    await set_user(response, user_id)
    return response


@router.get("/edit-item/{item_id}")
async def edit_item_form(request: Request, item_id: str, user_id: str = Depends(get_user)):
    """
    Fetch a single item by its ID for editing and render it using the 'edit_item_row.html' template.

    Args:
        request (Request): The HTTP request object.
        item_id (str): The unique identifier of the item to edit.

    Returns:
        TemplateResponse: A template response with the details of the item to be edited.
    """
    item = await fetch_item(item_id)
    response = templates.TemplateResponse("edit_item_row.html", {"request": request,
                                                             "input_types": Input_Types,
                                                             "item": item})
    await set_user(response, user_id)
    return response


@router.post("/add-item")
async def create_item(name_in: str = Form(...), 
                      description_in: str = Form(...), 
                      drawing_in: str = Form(...), 
                      quantity_in: int = Form(...), 
                      status_in: str = Form(...),
                      user_id: str = Depends(get_user)):
    """
    Create a new item in the inventory.

    Args:
        name_in (str): The name of the new item.
        description_in (str): The description of the new item.
        drawing_in (str): The drawing reference for the new item.
        quantity_in (int): The quantity of the new item.
        status_in (str): The status of the new item.

    Returns:
        RedirectResponse: Redirects to the inventory page after the item is added.
    """
    new_item = Item(name=name_in,
                description=description_in,
                drawing=drawing_in,
                quantity=quantity_in,
                status=status_in,
                user_id=user_id,
                update_date=datetime.now(),
                )
    await add_item(new_item)
    response = RedirectResponse(url="/", status_code=303)
    await set_user(response, user_id)
    return response


@router.put("/update-item/{item_id}")
async def update_item_edit(request: Request, item_id: str, 
                           description_in: str = Form(...), 
                           drawing_in: str = Form(...), 
                           quantity_in: int = Form(...), 
                           status_in: str = Form(...),
                           user_id: str = Depends(get_user)):
    """
    Update an existing item in the inventory.

    Args:
        request (Request): The HTTP request object.
        item_id (str): The unique identifier of the item to be updated.
        description_in (str): The new description of the item.
        drawing_in (str): The new drawing reference for the item.
        quantity_in (int): The new quantity of the item.
        status_in (str): The new status of the item.

    Returns:
        TemplateResponse: A template response with updated details of the item.
    """
    up_item = UpdateItem(description=description_in,
                         drawing=drawing_in,
                         quantity=quantity_in,
                         status=status_in,
                         user_id=user_id,
                         update_date=datetime.now(),
                         )
    await update_item(item_id, up_item)
    item = await fetch_item(item_id)
    response = templates.TemplateResponse("view_item_row.html", {"request": request, 
                                                             "item_schema": item_schema,
                                                             "item": item})
    await set_user(response, user_id)
    return response


@router.delete("/delete-item/{item_id}")
async def delete_item_edit(item_id: str, user_id: str = Depends(get_user)):
    """
    Delete an item from the inventory.

    Args:
        item_id (str): The unique identifier of the item to be deleted.

    Returns:
        Response: An empty response indicating successful deletion.
    """
    await delete_item(item_id)
    response = Response()
    await set_user(response, user_id)
    return response
