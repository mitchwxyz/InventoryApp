from pydantic import BaseModel
from datetime import datetime


class Item(BaseModel):
    """
    A Pydantic model representing an item.

    Attributes:
        name (str): The name of the item.
        description (str): A brief description of the item.
        drawing (str): A reference or identifier for a drawing related to the item.
        quantity (int): The quantity of the item in stock.
        status (str): The current status of the item (e.g., available, out of stock).
        update_date (datetime): set at time of DB transaction
        update_by (UserID): tbd
    """
    name: str
    description: str
    drawing: str
    quantity: int
    status: str
    user_id: str | None = None
    update_date: datetime | None = None


class UpdateItem(BaseModel):
    """
    A Pydantic model for updating an existing item. 
    This model excludes the 'name' field as it's assumed that the item's name does not change.
    """
    description: str
    drawing: str
    quantity: int
    status: str
    user_id: str | None = None
    update_date: datetime | None = None


Input_Types = {
    "name": {
        "type": "text",
        "no_update": True
    },
    "description": {
        "type": "text",
    },
    "drawing": {
        "type": "text",
    },
    "quantity": {
        "type": "number",
    },
    "status": {
        "type": "select",
        "options": ["Active", "Unavailable", "Slow"]
    },
}
