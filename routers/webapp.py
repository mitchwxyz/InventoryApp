from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, Response

from database import fetch_inventory_page, fetch_item, add_item, update_item, delete_item, search_items
from models import Item, UpdateItem

router = APIRouter(
    prefix="/app",
    tags=["App"],
    include_in_schema=False,
)

templates = Jinja2Templates(directory="templates")

ITEMS_PER_PAGE = 30

@router.get("/")
async def get_inventory(request: Request, page: int = 1):
    items = await fetch_inventory_page(page, ITEMS_PER_PAGE)
    return templates.TemplateResponse("base.html", {"request": request, "items": items, "current_page": 1})

@router.get("/items")
async def more_inventory(request: Request, page: int, search: str | None):
    if search:
        items = await search_items(search, page, ITEMS_PER_PAGE)
    else:
        items = await fetch_inventory_page(page, ITEMS_PER_PAGE)
    return templates.TemplateResponse("more_rows.html", {"request": request, "items": items, "current_page": page, "search": search})

@router.get("/item/{item_id}")
async def get_item(request: Request, item_id: str):
    item = await fetch_item(item_id)
    return templates.TemplateResponse("view_item_row.html", {"request": request, "item": item})

@router.post("/search")
async def search_name(request: Request, search: str = Form(None)):
    if search:
        items = await search_items(search, 1, ITEMS_PER_PAGE)
    else: items = await fetch_inventory_page(1, ITEMS_PER_PAGE)
    return templates.TemplateResponse("inventory.html", {"request": request, "items": items, "current_page": 1, "search": search})

@router.get("/edit-item/{item_id}")
async def edit_item_form(request: Request, item_id: str):
    item = await fetch_item(item_id)
    return templates.TemplateResponse("edit_item_row.html", {"request": request, "item": item})

@router.post("/add-item")
async def create_item(name_in: str = Form(...), description_in: str = Form(...), drawing_in: str = Form(...), quantity_in: int = Form(...), status_in: str = Form(...)):
    item = Item(name=name_in,
                description=description_in,
                drawing=drawing_in,
                quantity=quantity_in,
                status=status_in,
                )
    await add_item(item)
    return RedirectResponse(url="/", status_code=303)

@router.put("/update-item/{item_id}")
async def update_item_edit(request: Request, item_id: str, description_in: str = Form(...), drawing_in: str = Form(...), quantity_in: int = Form(...), status_in: str = Form(...)):
    up_item = UpdateItem(description=description_in,
                         drawing=drawing_in,
                         quantity=quantity_in,
                         status=status_in,
                         )
    await update_item(item_id, up_item)
    item = await fetch_item(item_id)
    return templates.TemplateResponse("view_item_row.html", {"request": request, "item": item})

@router.delete("/delete-item/{item_id}")
async def delete_item_edit(item_id: str):
    await delete_item(item_id)
    return Response()
