from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str
    drawing: str
    quantity: int
    status: str

class UpdateItem(BaseModel):
    description: str
    drawing: str
    quantity: int
    status: str