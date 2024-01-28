from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, Response

from database import fetch_all_items, fetch_item, add_item, update_item, delete_item


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get_inventory(request: Request):
    items = await fetch_all_items()
    return templates.TemplateResponse("inventory.html", {"request": request, "items": items})

@app.get("/item/{name}")
async def get_item(request: Request, name: str):
    item = await fetch_item(name)
    return templates.TemplateResponse("item_row.html", {"request": request, "item": item})

@app.get("/edit-item/{name}")
async def edit_item_form(request: Request, name: str):
    item = await fetch_item(name)
    return templates.TemplateResponse("edit_item.html", {"request": request, "item": item})

@app.post("/add-item")
async def create_item(name: str = Form(...), description: str = Form(...), drawing: str = Form(...), quantity: int = Form(...), status: str = Form(...)):
    await add_item(name, description, drawing, quantity, status)
    return RedirectResponse(url="/", status_code=303)

@app.put("/update-item/{name}")
async def update_item_edit(request: Request, name: str, description: str = Form(...), drawing: str = Form(...), quantity: int = Form(...), status: str = Form(...)):
    await update_item(name, description, drawing, quantity, status)
    item = await fetch_item(name)
    return templates.TemplateResponse("item_row.html", {"request": request, "item": item})

@app.delete("/delete-item/{name}")
async def delete_item_edit(name: str):
    await delete_item(name)
    return Response()