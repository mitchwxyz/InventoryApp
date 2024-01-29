from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, Response

from database import fetch_all_items, fetch_item, add_item, update_item, delete_item



router = APIRouter(
    prefix="/app",
    tags=["App"],
    include_in_schema=False,
)

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_inventory(request: Request):
    items = await fetch_all_items()
    return templates.TemplateResponse("inventory.html", {"request": request, "items": items})

@router.get("/item/{name}")
async def get_item(request: Request, name: str):
    item = await fetch_item(name)
    return templates.TemplateResponse("view_item_row.html", {"request": request, "item": item})

@router.get("/edit-item/{name}")
async def edit_item_form(request: Request, name: str):
    item = await fetch_item(name)
    return templates.TemplateResponse("edit_item_row.html", {"request": request, "item": item})

@router.post("/add-item")
async def create_item(name: str = Form(...), description: str = Form(...), drawing: str = Form(...), quantity: int = Form(...), status: str = Form(...)):
    await add_item(name, description, drawing, quantity, status)
    return RedirectResponse(url="/", status_code=303)

@router.put("/update-item/{name}")
async def update_item_edit(request: Request, name: str, description: str = Form(...), drawing: str = Form(...), quantity: int = Form(...), status: str = Form(...)):
    await update_item(name, description, drawing, quantity, status)
    item = await fetch_item(name)
    return templates.TemplateResponse("view_item_row.html", {"request": request, "item": item})

@router.delete("/delete-item/{name}")
async def delete_item_edit(name: str):
    await delete_item(name)
    return Response()