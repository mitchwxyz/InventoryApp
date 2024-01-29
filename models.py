from pydantic import BaseModel


class Item(BaseModel):
    name: str
    desription: str
    drawing: str
    quantity: int
    status: str